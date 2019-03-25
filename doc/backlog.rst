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
- [o] Error when starting with tmux on GKE: ``open terminal failed: not a terminal``
- [o] Add HTTP-/m3u8-based watcher
- [o] Make renditions selectable and configurable
- [o] Run "stress" to apply more load to system
- [o] How to install on trimmed-down runtime image without using "pip" at all?

Prio 2
======
- [o] Add option for controlling "packager" verbosity
- [o] Add option for displaying the pipeline commands
- [o] "iotop" bails out on GKE pods
- [o] Improve "About" / "Goals" section in README.rst
- [o] Talk about the "stress" tools
- [o] Talk about how to manually call into the K8s cluster
  with htop, glances and the watcher.
- [o] Capture ffmpeg progress output and maybe more
- [o] Optionally resume pipeline commands after crashing
- [o] Build ``mediatoolbox/avbroadcast:analyzer-edge`` which clones ``avbroadcast`` from
- [o] Terminate pipeline on exit of element, eventually signalling a failed pod.
- [o] Enable mouse in tmux
- [o] Indicate pipeline is running when blocking with CTRL+C message on pipeline start
- [o] Probe stream input before starting the pipeline
  ``ffprobe rtmp://de-origin-live.3qsdn.com/live/_definst_/mp4:6028_KcqnH2R6hyLbT4M``
- [o] Probe HLS output after starting the pipeline
  ``ffprobe /var/spool/hls-local/3q-test.m3u8``


Prio 3
======
- [o] Use sequential port numbering
- [o] Add runtime reporting and signalling
- [o] Add "avbroadcast" info
- [o] Run Shaka Packager through Vagrant
- [o] Add ``avbroadcast-installer.sh`` which runs ``alias avbroadcast`` through a wget -O- | curl
- [o] Add telemetry
- [o] Control process priorities
- [o] Analyze behavior under artifical system stress
- [o] Improve docs & credits
- [o] K8s alias
- [o] K8s double attach: ``tmux att -t avb``::

    kubectl exec --stdin --tty $pods -- tmux att -t avb

- [o] Look at "env" variables on pod
- [o] Jobfile in JSON format containing job configuration and runtime settings
- [o] How do I access the Kubernetes api from within a pod container?
  https://stackoverflow.com/questions/30690186/how-do-i-access-the-kubernetes-api-from-within-a-pod-container/30739416#30739416

::

    [rtmp @ 0x1491940] Server error: Failed to play 6028_KcqnH2R6hyLbT4M; stream not found.                │
    rtmp://de-origin-live.3qsdn.com/low/_definst_/mp4:6028_KcqnH2R6hyLbT4M: Operation not permitted        │
    Exception in thread Thread-1:                                                                          │
    Traceback (most recent call last):                                                                     │
      File "/usr/lib/python3.5/threading.py", line 914, in _bootstrap_inner                                │
        self.run()                                                                                         │
      File "/usr/local/lib/python3.5/dist-packages/avbroadcast-0.7.1-py3.5.egg/avbroadcast/core.py", line 8│
    5, in run                                                                                              │
        logger.write(proc.stdout.read())                                                                   │
    AttributeError: 'Logger' object has no attribute 'write'


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
- [o] Frame-based threading vs. sliced-threading:
  https://stackoverflow.com/questions/33624016/why-sliced-thread-affect-so-much-on-realtime-encoding-using-ffmpeg-x264
- [o] Use -tune xyz and --slice-threads

::

    # Setup
    apt install stress htop iotop tmux

    # Spawn looking glass
    tmux new -s toptop 'htop' \; split-window 'iotop' \; select-layout even-horizontal

    # Apply workload
    stress --cpu 4 --io 4 --timeout 60


*************
Documentation
*************
- https://tools.ietf.org/html/draft-pantos-http-live-streaming-20
-