#!/bin/bash

# Upgrade "avbroadcast"
/boot/avbroadcast-upgrade

# Report about system environment and software releases at runtime.
avsysinfo

# Propagate errors.
# Exit immediately if a command exits with a non-zero status.
set -e

# Run designated command.
exec "$@"
