# -*- coding: utf-8 -*-
# avbroadcast - republish audio/video streams for mass consumption
# (c) 2018 Andreas Motl <andreas.motl@elmyra.de>
import os
import re
import sys
import getopt
import textwrap
import tempfile
import unicodedata


def sanitize_text(text):
    text = textwrap.dedent(text)
    text = text.strip()
    return text


def read_options():
    # https://docs.python.org/3/library/getopt.html
    option_spec_short = "hsb:v"
    option_spec_long = ["help", "stream=", "base-port="]
    try:
        opts, args = getopt.getopt(sys.argv[1:], option_spec_short, option_spec_long)

    except getopt.GetoptError as err:
        # print help information and exit:
        #print(err)  # will print something like "option -a not recognized"
        #sys.exit(2)
        raise

    options = {}
    verbose = False
    for option, value in opts:
        #value = value.decode('utf-8')
        if option == "-v":
            verbose = True
        elif option in ("-h", "--help"):
            print("RTFM!")
            sys.exit()
        elif option in ("-s", "--stream"):
            options['stream'] = value
        elif option in ("-b", "--base-port"):
            options['base-port'] = int(value)
        else:
            assert False, "unhandled option"

    # Sanity checks
    if 'stream' not in options:
        raise getopt.GetoptError("--stream option required")
    if 'base-port' not in options:
        raise getopt.GetoptError("--stream option required")

    return options


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
