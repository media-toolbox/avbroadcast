# -*- coding: utf-8 -*-
# avbroadcast - republish media streams for mass consumption
# (c) 2019 Andreas Motl <andreas.motl@elmyra.de>
import os
import m3u8
import logging
from collections import OrderedDict


log = logging.getLogger(__name__)


class HLSInfo:

    def __init__(self, uri):
        self.uri = uri
        try:
            self.m3u8 = m3u8.load(uri)
        except FileNotFoundError as ex:
            log.error('Could not open .m3u8 file "%s"', self.uri)
            raise

    def get_info(self):
        info = OrderedDict()
        info['uri'] = self.uri
        info['streams'] = self.get_streams()
        info['segments'] = self.get_segments()
        return info

    def get_status(self, verbose=False):
        status = []
        for stream in self.get_streams():
            item = OrderedDict()
            item['name'] = os.path.basename(stream['uri'])
            item['bw'] = stream['info'].get('bandwidth')
            item['bwavg'] = stream['info'].get('average_bandwidth')
            item['segments'] = len(stream['segments'])
            try:
                item['first'] = '{} ({})'.format(
                    os.path.basename(stream['segments'][0]['uri']),
                    stream['segments'][0]['duration'],
                )
                item['last'] = '{} ({})'.format(
                    os.path.basename(stream['segments'][-1]['uri']),
                    stream['segments'][-1]['duration'],
                )
            except IndexError as ex:
                log.warning('Unable to read segments for "{}"'.format(stream['uri']))
            status.append(item)

        return status

    def get_status_compact(self):
        status = []
        for stream in self.get_streams():
            item = OrderedDict()
            if 'resolution' in stream['info']:
                item['kind'] = str(stream['info']['resolution'][1]) + 'p'
            else:
                item['kind'] = stream['info']['type']
            item['segments'] = len(stream['segments'])

            try:
                item['last'] = '{} ({})'.format(
                    os.path.basename(stream['segments'][-1]['uri']),
                    stream['segments'][-1]['duration'],
                )
            except IndexError as ex:
                log.warning('Unable to read segments for "{}"'.format(stream['uri']))

            item['bw'] = stream['info'].get('bandwidth')
            item['bwavg'] = stream['info'].get('average_bandwidth')
            status.append(item)

        return status

    def get_streams(self):
        streams = []

        # Collect audio streams.
        for item in self.m3u8.media:
            stream = OrderedDict()
            stream['uri'] = item.absolute_uri
            stream['info'] = dict(item.__dict__)
            stream['segments'] = HLSInfo(item.absolute_uri).get_segments()
            streams.append(stream)

        # Collect video streams.
        # TODO: Collect list of related Media entries from `media` attribute.
        for item in self.m3u8.playlists:
            stream = OrderedDict()
            stream['uri'] = item.absolute_uri
            stream['info'] = dict(item.stream_info._asdict())
            stream['segments'] = HLSInfo(item.absolute_uri).get_segments()
            streams.append(stream)

        # TODO: Also collect streams from `iframe_playlists`.

        return streams

    def get_segments(self):
        items = []
        for segment in self.m3u8.segments:
            item = {
                'uri': segment.absolute_uri,
                'duration': segment.duration,
            }
            items.append(item)

        return items
