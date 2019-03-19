#!/bin/bash

# TODO: Add "nproc", "free -m"
echo "------------------------------------------"
echo "             Operating system             "
echo "------------------------------------------"
echo "Debian: " && cat /etc/debian_version && echo
echo "OS:" && cat /etc/lsb-release && echo


echo "------------------------------------------"
echo "             System information           "
echo "------------------------------------------"
echo "CPU cores:" && nproc && echo
echo "Memory:" && free -m && echo


echo "------------------------------------------"
echo "            Software foundation           "
echo "------------------------------------------"
echo "ffmpeg:" && ffmpeg -version
echo "packager:" && packager --version
echo "Python:" && python3 --version
echo "avbroadcast:" && avbroadcast --version


echo "------------------------------------------"
