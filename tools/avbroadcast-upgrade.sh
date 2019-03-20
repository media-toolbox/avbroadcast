#!/bin/bash

echo "=========================================="
echo "                avbroadcast               "
echo "=========================================="

echo "Hello avbroadcast"

echo "Upgrading avbroadcast from PyPI"
pip3 install --upgrade avbroadcast

test -e /avbroadcast && (
    echo "Upgrading avbroadcast from development tree"
    cd /avbroadcast
    python3 setup.py --quiet install
)

# TODO: Upgrade from Git repository

echo
