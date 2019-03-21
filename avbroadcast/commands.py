# -*- coding: utf-8 -*-
# avbroadcast - republish media streams for mass consumption
# (c) 2018-2019 Andreas Motl <andreas.motl@elmyra.de>
import os
import sys
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
        {program} ingest --stream=<stream> [--base-port=<base-port>] [--verbose]
        {program} publish --name=<name> [--base-port=<base-port>] --target=<target> [--verbose]
        {program} io --name=<name> --stream=<stream> --target=<target> [--base-port=<base-port>] [--verbose] [--tmux] [--attach] [--analyze]
        {program} watch --path=<path>
        {program} info
        {program} --version
        {program} (-h | --help)

    Options:
        --base-port=<base-port>     Use this port as a baseline for forwarding the first UDP stream.
                                    [default: 50000]
        --verbose                   Increase verbosity
        --tmux                      Run inside tmux session
        --attach                    Attach to tmux session immediately
        --analyze                   Run more analyzers in tmux window

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
    logger.info('Options: %s', options)
    logger.info('Command: %s', ' '.join(list(sys.argv)))

    if options['tmux']:
        run_tmux(options)
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
        # TODO: Propagate renditions and interval.
        watch_filesystem(options['path'])


def run_tmux(options):
    """Run transcoder in tmux, optionally with instrumentation."""

    # Compute commandline of program invocation w/o "--tmux" parameter.
    real = list(sys.argv)
    real.remove('--tmux')
    real_command = ' '.join(real)

    # Wrap command into tmux command.
    # TODO: Just use "-d" for detach when running with "--background"
    tmux_command = "tmux new-session -d -s avb '{}'".format(real_command)

    if options['analyze']:

        # Add system performance metrics tools.
        # TODO: Add iotop. However, this does not work on k8s?
        # select-layout even-horizontal
        tmux_command += " \; split-window 'htop --delay=3' \; split-window -h 'glances --percpu --time=1.5'"

        # Add file watcher if output target is a local directory.
        if options['target']:
            tmux_command += " \; select-pane -t0" \
                            " \; split-window -h 'avbroadcast watch --path={}'".format(options['target'])

    logger.info('tmux command: %s', tmux_command)
    os.system(tmux_command)

    # Attach to tmux session right away.
    # When running this on Docker, this will kill the container when detaching
    # from it, as we've previously exec'd into here, so we just are PID 1.
    # Remark: This will only work when having a TTY in place.
    # TODO: Just use when running with "--attach"
    if options['attach']:
        os.system('tmux attach -t avb')

    # Use "--keepalive" parameter here to keep the container alive even without
    # attaching immediately.
    # TODO: Just use when running with "--background" and without "--attach"?
    # TODO: How to escape from here? Actually, this should be bound to the aliveness
    # of the workhorse programs, right?

    # TODO: Display activity somehow.
    print
    print
    print('Transcoder is running. Will wait forever here.')
    print('Run "tmux attach -t avb" on a different shell to attach to tmux session.')
    print('Exit transcoder by typing CTRL+C.')
    wait_forever()


def wait_forever():
    from threading import Event
    Event().wait()
