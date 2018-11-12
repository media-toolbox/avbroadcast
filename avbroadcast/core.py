# -*- coding: utf-8 -*-
# avbroadcast - republish audio/video streams for mass consumption
# (c) 2018 Andreas Motl <andreas.motl@elmyra.de>
import os

from avbroadcast.util import sanitize_text, make_progress_filename


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
        -profile:v main {bandwidth} -level 31 \\
        -filter:a "pan=stereo|c0=c0|c1=c0" \\
        -f mpegts "{target}" -map 0:v
    """

    presets = [
        {
            'resolution': 1080,
            'bandwidth': '-b:v 4000k -maxrate 6000k -bufsize 4800k',
            'target': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 240,
            'bandwidth': '-b:v  450k -maxrate  675k -bufsize  540k',
            'target': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 360,
            'bandwidth': '-b:v  990k -maxrate 1485k -bufsize 1188k',
            'target': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 480,
            'bandwidth': '-b:v 1600k -maxrate 2400k -bufsize 1920k',
            'target': 'udp://127.0.0.1:{port}',
        },
        {
            'resolution': 720,
            'bandwidth': '-b:v 2000k -maxrate 3000k -bufsize 2400k',
            'target': 'udp://127.0.0.1:{port}',
        },
    ]

    def __init__(self, base_port=None, progress_file=None):
        self.base_port = base_port
        self.progress_file = progress_file

    def run(self, source):

        ffmpeg_base = sanitize_text(self.ffmpeg_base)
        data = {}
        data['source'] = source
        data['progress_file'] = self.progress_file
        ffmpeg_base = ffmpeg_base.format(**data)
        parts = [ffmpeg_base]

        for preset in self.presets:
            port = self.base_port + preset['resolution']

            data = preset.copy()
            data['port'] = port

            stream_part = sanitize_text(self.ffmpeg_video_stream).format(**data).format(**data)
            parts.append(stream_part)

        command = ' \\\n\\\n'.join(parts)
        print("ffmpeg command is:")
        print(command)
        print("Running ffmpeg")
        os.system(command)


def main():
    options = {'base-port': 50000, 'stream': 'rtmp://184.72.239.149/vod/mp4:bigbuckbunny_450.mp4?reuse=1'}

    base_port = options['base-port']
    progress_file = make_progress_filename(options['stream'])

    decoder = StreamDecoder(base_port=base_port, progress_file=progress_file)
    decoder.run(source=options['stream'])


if __name__ == '__main__':
    main()
