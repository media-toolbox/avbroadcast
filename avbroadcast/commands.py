# -*- coding: utf-8 -*-
# avbroadcast - republish media streams for mass consumption
# (c) 2018-2019 Andreas Motl <andreas.motl@elmyra.de>
import logging
import os
import sys

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
        {program} ingest --stream=<stream> [--base-port=<base-port>] [--verbose]
        {program} publish --name=<name> [--base-port=<base-port>] --target=<target> [--verbose]
        {program} io --name=<name> --stream=<stream> --target=<target> [--base-port=<base-port>] [--verbose] [--tmux] [--analyze]
        {program} watch --path=<path>
        {program} info
        {program} --version
        {program} (-h | --help)

    Options:
        --base-port=<base-port>     Use this port as a baseline for forwarding the first UDP stream.
                                    [default: 50000]
        --verbose                   Increase verbosity

    Examples:

        # Ingest media stream from RTMP.
        avbroadcast ingest --stream="rtmp://184.72.239.149/vod/mp4:bigbuckbunny_450.mp4?reuse=1" --base-port=50000

        # Package using HLS and publish to local file system.
        avbroadcast publish --name="bigbuckbunny" --base-port=50000 --target="/var/spool/hls-local"

        # Watch output directory
        avbroadcast watch --path=/var/spool/hls-local

        # Package using HLS and publish to HTTP server.
        avbroadcast publish --name="bigbuckbunny" --base-port=50000 --target="http://localhost:6767/hls-live"

    """

    # Use generic commandline options schema and amend with current program name.
    commandline_schema = run.__doc__.format(program=APP_NAME)

    d = docopt(commandline_schema, version=APP_NAME + ' ' + __version__)

    # Read commandline options.
    options = normalize_options(docopt(commandline_schema, version=APP_NAME + ' ' + __version__))

    # Start logging subsystem.
    if options['verbose']:
        options['debug'] = True
    boot_logging(options)

    # Report about runtime options.
    logger.info(options)

    # tmux new -s toptop 'htop' \; split-window 'iotop' \; select-layout even-horizontal
    # tmux attach -t avb \; split-window htop --delay=3 \; split-window -h glances --time=0.3
    # select-pane -t0
    if options['tmux']:
        real = list(sys.argv)
        real.remove('--tmux')
        real_command = ' '.join(real)
        #print(real_command)
        #tmux_command = "tmux -2 new-session -s avb \; new-window -t avb '{}'".format(real_command)
        tmux_command = "tmux new-session -s avb '{}'".format(real_command)

        if options['analyze']:
            tmux_command += ' \; split-window htop --delay=3 \; split-window -h glances --time=0.3'
            tmux_command += ' \; select-pane -t0 \; split-window -h avbroadcast watch --path=/var/spool/hls-local'

        print(tmux_command)
        os.system(tmux_command)
        return

    # Dispatch to core methods.
    pipeline = RtmpHlsPipeline()
    if options['ingest']:
        pipeline.ingest(options['stream'], int(options['base-port']))

    if options['publish']:
        pipeline.publish(options['name'], int(options['base-port']), options['target'])

    if options['io']:
        pipeline.ingest(options['stream'], int(options['base-port']))
        pipeline.publish(options['name'], int(options['base-port']), options['target'])

    if options['watch']:
        # TODO: Propagate resolutions and interval
        watch_filesystem(options['path'])

    #if options['add-watch']:
    #    # TODO: Propagate resolutions and interval
    #    watch_filesystem(options['target'], clear_screen=False)
