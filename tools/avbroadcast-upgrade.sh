#!/bin/bash

echo "=========================================="
echo "                avbroadcast               "
echo "=========================================="

echo "Hello avbroadcast"

# Upgrade from Git repository
test "$1" = "git" && (
    echo "Upgrading avbroadcast from git repository"
    git clone --depth=1 https://github.com/media-toolkit/avbroadcast /avbroadcast
    cd /avbroadcast
    python3 setup.py install
) && exit

echo "Upgrading avbroadcast from PyPI"
pip3 install --upgrade avbroadcast

test -e /avbroadcast && (
    echo "Upgrading avbroadcast from development tree"
    cd /avbroadcast
    python3 setup.py --quiet install
)

echo
