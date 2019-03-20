###################
avbroadcast backlog
###################


*******
General
*******

Prio 1
======
- [x] Display relevant program versions (ffmpeg, packager)
- [x] Run Shaka Packager through Docker
- [x] tmux multiplexer as outlined plus command info and "glances --time 0.2"
- [x] Run through Docker by prefixing ``docker run -it --rm media-toolbox/avbroadcast-ubuntu``
- [x] Run pipeline commands hosted through Python threads
- [o] Make renditions selectable and configurable
- [o] Add option for controlling "packager" verbosity
- [o] Add option for displaying the pipeline commands
- [o] Error when starting with tmux on GKE::

    open terminal failed: not a terminal

- [o] "iotop" bails out on GKE pods
- [o] Improve "About" / "Goals" section in README.rst
- [o] Talk about the "stress" tools
- [o] Talk about how to manually call into the K8s cluster
  with htop, glances and the watcher.
- [o] Capture ffmpeg progress output and maybe more
- [o] Optionally resume pipeline commands after crashing
- [o] Build ``mediatoolbox/avbroadcast:analyzer-edge`` which clones ``avbroadcast`` from


Prio 2
======
- [o] Use sequential port numbering
- [o] Add runtime reporting and signalling
- [o] Add "avbroadcast" info
- [o] Run Shaka Packager through Vagrant


**********
K8s on GKE
**********
Investigate::

    CPUManager=true|false (BETA - default=true)
    CustomCPUCFSQuotaPeriod=true|false (ALPHA - default=false)
    # -- https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/


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
