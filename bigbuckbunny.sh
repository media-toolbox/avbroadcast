#!/bin/bash

# Ingest Big Buck Bunny stream in 450p using ffmpeg.
avbroadcast ingest \
    --stream="rtmp://184.72.239.149/vod/mp4:bigbuckbunny_450.mp4?reuse=1" \
    --base-port=50000 \
    --verbose

# Run Shaka Packager to produce HLS output.
