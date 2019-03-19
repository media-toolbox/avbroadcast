# -*- coding: utf-8 -*-
# (c) 2018-2019 Andreas Motl <andreas.motl@elmyra.de>
import logging
import os
import re
import sys
import getopt
import textwrap
import tempfile
import unicodedata


def boot_logging(options=None):
    log_level = logging.INFO
    if options and options.get('debug'):
        log_level = logging.DEBUG
    setup_logging(level=log_level)


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-20s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)


def normalize_options(options):
    normalized = {}
    for key, value in options.items():
        key = key.strip('--<>')
        normalized[key] = value
    return normalized


def sanitize_text(text):
    text = textwrap.dedent(text)
    text = text.strip()
    return text


def slugify(value):
    """
    Slugify function from django.utils.text, slightly modified.

    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.

    https://stackoverflow.com/questions/5574042/string-slugification-in-python/27264385#27264385
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '-', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value


def make_progress_filename(uri):
    dirname = tempfile.gettempdir()
    filename = slugify(uri) + '.ffmpeg.progress'
    filepath = os.path.join(dirname, filename)
    return filepath
