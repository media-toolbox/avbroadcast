# -*- coding: utf-8 -*-
# avbroadcast - republish media streams for mass consumption
# (c) 2018 Andreas Motl <andreas.motl@elmyra.de>
import logging

from docopt import docopt
from avbroadcast import __version__

from avbroadcast.core import InputStream, RtmpHlsPipeline
from avbroadcast.util import make_progress_filename, normalize_options, boot_logging
from avbroadcast.watch import watch_filesystem

logger = logging.getLogger(__name__)

APP_NAME = 'avbroadcast'


def run():
    """
    Usage:
        {program} ingest --stream=<stream> --base-port=<base-port> [--verbose]
        {program} publish --name=<name> --base-port=<base-port> --target=<target> [--verbose]
        {program} watch --path=<path>
        {program} info
        {program} --version
        {program} (-h | --help)

    Options:
        --verbose     Increase verbosity

    Examples:

        # Ingest media stream
        avbroadcast ingest \
            --stream="rtmp://184.72.239.149/vod/mp4:bigbuckbunny_450.mp4?reuse=1" \
            --base-port=50000

        # Package using HLS and publish to HTTP server
        avbroadcast publish \
            --name="bigbuckbunny" \
            --base-port=50000 \
            --target="/var/spool/hls-local"

        # Watch output directory
        avbroadcast watch --path=/var/spool/hls-local


    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = (run.__doc__).format(program=APP_NAME)

    # Read commandline options
    options = normalize_options(docopt(commandline_schema, version=APP_NAME + ' ' + __version__))

    # Start logging subsystem
    if options['verbose']:
        options['debug'] = True
    boot_logging(options)

    # Dispatch to core methods
    pipeline = RtmpHlsPipeline()
    if options['ingest']:
        pipeline.ingest(options['stream'], int(options['base-port']))

    if options['publish']:
        pipeline.publish(options['name'], int(options['base-port']), options['target'])

    if options['watch']:
        # TODO: Propagate resolutions and interval
        watch_filesystem(options['path'])
