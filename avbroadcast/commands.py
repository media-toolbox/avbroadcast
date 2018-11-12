# -*- coding: utf-8 -*-
# avbroadcast - republish audio/video streams for mass consumption
# (c) 2018 Andreas Motl <andreas.motl@elmyra.de>
import logging

from docopt import docopt
from avbroadcast import __version__

from avbroadcast.core import StreamDecoder, RtmpHlsPipeline
from avbroadcast.util import make_progress_filename, normalize_options, boot_logging

logger = logging.getLogger(__name__)

APP_NAME = 'avbroadcast'


def run():
    """
    Usage:
        {program} ingest --stream=<stream> --base-port=<base-port> --debug
        {program} info
        {program} --version
        {program} (-h | --help)

    Options:
        --debug     Increase verbosity

    Examples:

        # Ingest Big Buck Bunny stream in 450p
        avbroadcast \
            --stream="rtmp://184.72.239.149/vod/mp4:bigbuckbunny_450.mp4?reuse=1" \
            --base-port=50000
    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = (run.__doc__).format(program=APP_NAME)

    # Read commandline options
    options = normalize_options(docopt(commandline_schema, version=APP_NAME + ' ' + __version__))

    # Start logging subsystem
    boot_logging(options)

    # Dispatch to core methods
    if 'ingest' in options:
        pipeline = RtmpHlsPipeline()
        pipeline.ingest(options['stream'], int(options['base-port']))
