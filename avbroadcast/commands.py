# -*- coding: utf-8 -*-
# avbroadcast - republish audio/video streams for mass consumption
# (c) 2018 Andreas Motl <andreas.motl@elmyra.de>
from avbroadcast.core import StreamDecoder
from avbroadcast.util import read_options, make_progress_filename


def run():
    options = read_options()

    base_port = options['base-port']
    progress_file = make_progress_filename(options['stream'])

    decoder = StreamDecoder(base_port=base_port, progress_file=progress_file)
    decoder.run(source=options['stream'])
