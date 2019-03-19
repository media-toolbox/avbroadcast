#!/bin/bash

echo "Hello avbroadcast"

echo "Upgrading avbroadcast from PyPI"
pip3 install --upgrade avbroadcast

echo "Upgrading avbroadcast from development tree"
test -e /avbroadcast && cd /avbroadcast; python3 setup.py --quiet install
