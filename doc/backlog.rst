###################
avbroadcast backlog
###################

- [o] Display relevant program versions (ffmpeg, packager)
- [o] Add Vagrantfile
- [o] Run Shaka Packager through Docker or Vagrant

- [o] Use sequential port numbering
- [o] Add option for controlling "packager" verbosity
- [o] Add runtime reporting and signalling

- [o] Run pipeline artefacts with the "multiprocessing" module:
  https://docs.python.org/3/library/multiprocessing.html

- [o] tmux multiplexer as outlined plus command info and "glances --time 0.2"
- [o] Add "avbroadcast" info
- [o] Run through Docker by prefixing docker run -it --rm daq-tools/avbroadcast-ubuntu


******
ffmpeg
******
- [o] Follow ffmpeg parameter recommendations from
  https://google.github.io/shaka-packager/html/tutorials/encoding.html
- [o] Set ffmpeg ``buffer_size=`` argument on input source, see
  https://google.github.io/shaka-packager/html/tutorials/live.html#udp-file-options
- [o] Use -tune xyz and -slice-threads

::

    # Setup
    apt install stress htop iotop tmux

    # Spawn looking glass
    tmux new -s toptop 'htop' \; split-window 'iotop' \; select-layout even-horizontal

    # Apply workload
    stress --cpu 4 --io 4 --timeout 60
