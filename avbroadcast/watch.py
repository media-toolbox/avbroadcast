# -*- coding: utf-8 -*-
# avbroadcast - republish media streams for mass consumption
# (c) 2019 Andreas Motl <andreas.motl@elmyra.de>
import os
import time
import logging

log = logging.getLogger(__name__)

APP_NAME = 'avbroadcast'


def watch_filesystem(path, resolutions=None, clear_screen=True, interval=0.5):
    while True:
        if clear_screen:
            os.system('clear')
        log.info('Scanning {path} each {interval} seconds.'.format(path=path, interval=interval))

        scan_filesystem(path, resolutions=resolutions)
        time.sleep(interval)


def scan_filesystem(path, resolutions=None):
    resolutions = resolutions or "144 240 360 480 720 1080"
    for resolution in resolutions.split(' '):
        command = 'ls {path} | grep "\-{resolution}\-" | sort | tail -n1'.format(path=path, resolution=resolution)
        os.system(command)
