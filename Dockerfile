ARG BASE_IMAGE

# ==============
# Baseline image
# ==============
FROM jrottenberg/ffmpeg:4.0-ubuntu AS ffmpeg-runtime


# ==========================
# Performance analysis image
# ==========================

# Derive image from regular runtime image.
FROM ffmpeg-runtime AS avbroadcast-analyzer

# Install performance analysis tools.
RUN apt-get update
RUN apt-get install -y stress htop iotop tmux glances psmisc


# =============
# Runtime image
# =============
FROM ${BASE_IMAGE} AS avbroadcast-runtime

LABEL maintainer="andreas.motl@elmyra.de"
LABEL title="Runtime for avbroadcast"
LABEL description="Republish media streams for mass consumption using ffmpeg and Shaka Packager"

# Downlad URL to custom Shaka Packager.
ARG SHAKA_PACKAGER_DOWNLOAD_URL=https://packages.elmyra.de/3q/foss/packager-linux-http-upload


# Regular runtime.
RUN apt-get update
RUN apt-get install -y python3 python3-pip wget nano vim

# Install Shaka Packager.
RUN \
    wget --quiet --output-document /usr/local/bin/packager ${SHAKA_PACKAGER_DOWNLOAD_URL} && \
    chmod +x /usr/local/bin/packager

COPY tools/avsysinfo.sh /usr/local/bin/avsysinfo

# Install avbroadcast.
ENV LANG=C.UTF-8
RUN pip3 install --upgrade pip
RUN pip3 install avbroadcast

#
COPY tools/avbroadcast-upgrade.sh /boot/avbroadcast-upgrade
COPY tools/docker-entrypoint.sh /boot/docker-entrypoint

# Report about system environment and software releases at build-time.
RUN avsysinfo

ENTRYPOINT ["/boot/docker-entrypoint"]
CMD ["echo", "Running avbroadcast in Docker container"]
