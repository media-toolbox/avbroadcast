.. image:: https://img.shields.io/badge/Python-3.5,%203.6,%203.7,%203.8-green.svg
    :target: https://pypi.org/project/avbroadcast/

.. image:: https://img.shields.io/pypi/v/avbroadcast.svg
    :target: https://pypi.org/project/avbroadcast/

.. image:: https://img.shields.io/github/tag/media-toolbox/avbroadcast.svg
    :target: https://github.com/media-toolbox/avbroadcast

|


###########
avbroadcast
###########


*****
About
*****
``avbroadcast`` republishes media streams for mass consumption.
It is a wrapper around the fine ffmpeg_ and packager_ programs,
so it is standing on the shoulders of giants.

.. _ffmpeg: https://ffmpeg.org/
.. _packager: https://github.com/google/shaka-packager/


.. attention::

    Please note some of its functionality is based on the new `HTTP upload feature`_
    of Shaka Packager which is a work in progress. It is currently living
    in the `http-upload branch`_ and is being tracked at `issue #149`_.

    Please use the beta-build `packager-linux`_ for your own experiments,
    which is also available through the corresponding Docker baseline image.

.. _HTTP upload feature: https://github.com/3QSDN/shaka-packager/blob/http-upload/docs/source/tutorials/http_upload.rst
.. _issue #149: https://github.com/google/shaka-packager/issues/149
.. _http-upload branch: https://github.com/3QSDN/shaka-packager/tree/http-upload
.. _packager-linux: https://packages.elmyra.de/3q/foss/packager-linux-http-upload


***************
Getting started
***************

Install
=======
If you know your way around Python, installing this software is really easy::

    pip install avbroadcast

Please refer to the `virtualenv`_ page about further guidelines how to install and use this software.

.. _virtualenv: https://github.com/media-toolbox/avbroadcast/blob/master/doc/virtualenv.rst


Usage
=====
Ingest media stream::

    avbroadcast ingest \
        --stream="rtmp://184.72.239.149/vod/mp4:bigbuckbunny_450.mp4?reuse=1" \
        --base-port=50000 \
        --verbose

Package using HLS and publish to HTTP server::

    avbroadcast publish \
        --name="bigbuckbunny" \
        --base-port=50000 \
        --target="http://localhost:6767/hls-live" \
        --verbose

Altogether now::

    avbroadcast io \
        --name="bigbuckbunny" \
        --stream="rtmp://184.72.239.149/vod/mp4:bigbuckbunny_450.mp4?reuse=1" \
        --target="http://localhost:6767/hls-live" \
        --verbose

Watch output directory::

    avbroadcast watch --path=/var/spool/hls-local


Usage with Docker
=================
Build Docker image ``"mediatoolbox/avbroadcast:analyzer"``::

    make build-docker-image

You might want to skip this step as Docker images are already available
at https://hub.docker.com/r/mediatoolbox/avbroadcast

Make alias for easy access::

    # Use avbroadcast shipped with Docker image.
    alias avbroadcast='docker run --name avb --interactive --tty --rm mediatoolbox/avbroadcast:analyzer avbroadcast'

    # Alternatively, use avbroadcast from working tree.
    alias avbroadcast='docker run --name avb --volume `pwd`:/avbroadcast --interactive --tty --rm mediatoolbox/avbroadcast:analyzer avbroadcast'

Pre-flight check::

    avbroadcast --version

Attach to running transcoder::

    docker exec --interactive --tty avb /bin/bash


Usage with tmux
===============
::

    avbroadcast ... --tmux --analyze

Attach to Docker container and tmux manager at once::

    docker exec --interactive --tty avb tmux attach -t avb

Quit pipeline either by detaching from ``tmux``::

    CTRL+B, D

or exit each program individually by typing::

    4x CTRL+C

In both cases, the Docker container will stop - and also self-destroy when running with ``--rm``.


*******************
Project information
*******************
``avbroadcast`` is released under the terms of the GNU AGPL 3.0 license.
The code and documentation live on `GitHub <https://github.com/media-toolbox/avbroadcast>`_,
the Python package is published to `PyPI <https://pypi.org/project/avbroadcast/>`_.

The software has been tested on Python 3.5 and Python 3.7.

Contributing
============
If you'd like to contribute you're most welcome!
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.

Thanks in advance for your efforts, we really appreciate any help or feedback.

License
=======
This software is copyright (c) 2018-2019 The avbroadcast authors. All rights reserved.

It is and will always be **free and open source software**.

Use of the source code included here is governed by the
`GNU Affero General Public License <GNU-AGPL-3.0_>`_ and the
`European Union Public License <EUPL-1.2_>`_.

.. _GNU-AGPL-3.0: https://github.com/media-toolbox/avbroadcast/blob/master/LICENSE
.. _EUPL-1.2: https://opensource.org/licenses/EUPL-1.1


----

Have fun!
