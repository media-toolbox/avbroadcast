# -*- coding: utf-8 -*-
# avbroadcast - republish media streams for mass consumption
# (c) 2018 Andreas Motl <andreas.motl@elmyra.de>
import os
import logging

from avbroadcast.util import sanitize_text, make_progress_filename

logger = logging.getLogger(__name__)


class RtmpHlsPipeline:

    presets = [
        {
            'resolution': 1080,
            'ffmpeg_bandwidth': '-b:v 4000k -maxrate 6000k -bufsize 4800k',
            'target': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 240,
            'ffmpeg_bandwidth': '-b:v  450k -maxrate  675k -bufsize  540k',
            'target': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 360,
            'ffmpeg_bandwidth': '-b:v  990k -maxrate 1485k -bufsize 1188k',
            'target': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 480,
            'ffmpeg_bandwidth': '-b:v 1600k -maxrate 2400k -bufsize 1920k',
            'target': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 720,
            'ffmpeg_bandwidth': '-b:v 2000k -maxrate 3000k -bufsize 2400k',
            'target': 'udp://127.0.0.1:{port}',
        },
    ]

    def stream_descriptions(self, base_port):
        for preset in self.presets:

            stream = preset.copy()
            port = base_port + preset['resolution']
            stream['target'] = stream['target'].format(port=port)

            yield stream

    def ingest(self, stream, base_port):
        decoder = StreamDecoder(source=stream, base_port=base_port)
        decoder.run(presets=self.stream_descriptions(base_port))


class StreamDecoder:

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

    # {resolution}p video is streamed to {target}
    ffmpeg_video_stream = """
        -vf scale="trunc(oh*a/2)*2:{resolution}" \\
        -map_metadata -1 -pix_fmt yuv420p -vcodec libx264 -preset:v superfast \\
        -force_key_frames "expr:gte(t,n_forced*2)" \\
        -x264opts ref=1:no-cabac=1:bframes=0:b-pyramid=0:scenecut=0 -sc_threshold 0 \\
        -profile:v main {ffmpeg_bandwidth} -level 31 \\
        -filter:a "pan=stereo|c0=c0|c1=c0" \\
        -f mpegts "{target}" -map 0:v
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

    def run(self, presets):
        command = self.get_command(presets)
        logger.debug("Running ffmpeg command:\n%s", command)
        os.system(command)
