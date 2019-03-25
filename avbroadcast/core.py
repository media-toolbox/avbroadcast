# -*- coding: utf-8 -*-
# avbroadcast - republish media streams for mass consumption
# (c) 2018-2019 Andreas Motl <andreas.motl@elmyra.de>
import shlex
import logging
import subprocess
from threading import Thread

from avbroadcast.util import sanitize_text, make_progress_filename

logger = logging.getLogger(__name__)


class RtmpHlsPipeline:

    presets = [
        {
            'resolution': 1080,
            'ffmpeg_bandwidth': '-b:v 4000k -maxrate 6000k -bufsize 4800k',
            'address': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 144,
            'ffmpeg_bandwidth': '-b:v  100k -maxrate  150k -bufsize  120k',
            'address': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 240,
            'ffmpeg_bandwidth': '-b:v  450k -maxrate  675k -bufsize  540k',
            'address': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 360,
            'ffmpeg_bandwidth': '-b:v  990k -maxrate 1485k -bufsize 1188k',
            'address': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 480,
            'ffmpeg_bandwidth': '-b:v 1600k -maxrate 2400k -bufsize 1920k',
            'address': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 720,
            'ffmpeg_bandwidth': '-b:v 2000k -maxrate 3000k -bufsize 2400k',
            'address': 'udp://127.0.0.1:{port}',
        },
    ]

    def stream_descriptions(self, base_port):
        for preset in self.presets:

            stream = preset.copy()
            port = base_port + preset['resolution']
            stream['address'] = stream['address'].format(port=port)

            yield stream

    def ingest(self, stream, base_port):
        decoder = InputStream(source=stream, base_port=base_port)
        command = decoder.configure(presets=self.stream_descriptions(base_port))

        pc = PipelineCommand(command)
        pc.start()

    def publish(self, name, base_port, upload_url):
        packager = OutputPackager(name=name, base_port=base_port, upload_url=upload_url)
        command = packager.configure(presets=self.stream_descriptions(base_port))

        pc = PipelineCommand(command)
        pc.start()


class PipelineCommand(Thread):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        cmd = list(map(str.strip, shlex.split(self.command)))
        #logger.debug(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        with process as proc:
            logger.write(proc.stdout.read())


class InputStream:

    # TODO: -report

    ffmpeg_base = """
        ffmpeg \\
        \\
        -fflags nobuffer \\
        -threads 0 -y -progress "{progress_file}" \\
        -i "{source}" \\
        \\
        -acodec aac -ac 2 -ar 48000 -b:a 128k
    """

    # {resolution}p video is streamed to {address}
    ffmpeg_video_stream = """
        -vf scale="trunc(oh*a/2)*2:{resolution}" \\
        -map_metadata -1 -pix_fmt yuv420p -vcodec libx264 -preset:v superfast \\
        -force_key_frames "expr:gte(t,n_forced*2)" \\
        -x264opts ref=1:no-cabac=1:bframes=0:b-pyramid=0:scenecut=0 -sc_threshold 0 \\
        -profile:v main {ffmpeg_bandwidth} -level 31 \\
        -filter:a "pan=stereo|c0=c0|c1=c0" \\
        -f mpegts "{address}" -map 0:v
    """

    def __init__(self, source=None, base_port=None):
        self.source = source
        self.base_port = base_port
        self.progress_file = make_progress_filename(source)

    def get_command(self, presets):

        ffmpeg_base = sanitize_text(self.ffmpeg_base)
        data = {}
        data['source'] = self.source
        data['progress_file'] = self.progress_file
        ffmpeg_base = ffmpeg_base.format(**data)
        parts = [ffmpeg_base]

        for preset in presets:
            stream_part = sanitize_text(self.ffmpeg_video_stream).format(**preset)
            parts.append(stream_part)

        command = ' \\\n\\\n'.join(parts)
        return command

    def configure(self, presets):
        command = self.get_command(presets)
        logger.debug("Running ffmpeg command:\n%s", command)

        #command_suffix = '1> {logfile} 2>&1'.format(logfile='/$TMPDIR/avbroadcast_ffmpeg_6028_2019-03-18_19-08-05.log')
        #command += command_suffix

        return command

        #command_suffix += ' &'
        #os.system(command)
        #os.execlp(command)

        #element = PipelineElement(command)
        #print(element)


class OutputPackager:

    packager_base = """
        packager \\
        --io_block_size 65536 --fragment_duration 2 --segment_duration 2 \\
        --time_shift_buffer_depth 3600 --preserved_segments_outside_live_window 7200 \\
        --hls_master_playlist_output "{upload_url}/{name}.m3u8" \\
        --hls_playlist_type LIVE \\
        --vmodule=file=1,http_file=1,media_playlist=1,hls_notify_muxer_listener=1,ts_segmenter=1,ts_writer=1
    """

    # TODO: Optionally add option "--libcurl_verbosity=3"
    # TODO: Optionally add "--vmodule" options "buffer_writer=1", "master_playlist=1" and "packed_audio_writer=1"

    packager_audio_stream = """
        "input={address}?reuse=1,stream=audio,segment_template={upload_url}/{name}-audio-128k-$Number%04d$.aac,playlist_name={name}-audio-128k.m3u8,hls_group_id=audio"
    """

    packager_video_stream = """
        "input={address}?reuse=1,stream=video,segment_template={upload_url}/{name}-video-{resolution:0>4}-$Number%04d$.ts,playlist_name={name}-video-{resolution:0>4}.m3u8"
    """

    newline_token = ' \\\n'

    def __init__(self, name=None, base_port=None, upload_url=None):
        self.name = name
        self.base_port = base_port
        self.upload_url = upload_url

    def get_command(self, presets):
        packager_base = sanitize_text(self.packager_base)

        data = {}
        data['name'] = self.name
        data['upload_url'] = self.upload_url
        packager_base = packager_base.format(**data)

        presets = list(presets)
        stream_parts = []

        # 1. Add audio stream from first channel
        first_preset = presets[0]
        stream_part = sanitize_text(self.packager_audio_stream).format(**data, **first_preset)
        stream_parts.append(stream_part)

        # 2. Add all video stream channels
        for preset in presets:
            stream_part = sanitize_text(self.packager_video_stream).format(**data, **preset)
            stream_parts.append(stream_part)

        all_streams = self.join_command(stream_parts)

        parts = [packager_base, all_streams]
        command = self.join_command(parts)
        return command

    def join_command(self, parts):
        return self.newline_token.join(parts)

    def configure(self, presets):
        command = self.get_command(presets)
        logger.debug("Running packager command:\n%s", command)

        #command_suffix = '1> {logfile} 2>&1'.format(logfile='/$TMPDIR/avbroadcast_packager_6028_2019-03-18_19-08-05.log')

        #os.system(command)
        return command
