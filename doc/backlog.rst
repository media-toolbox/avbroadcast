###################
avbroadcast backlog
###################

- [o] Follow ffmpeg parameter recommendations from [1]
- [o] Set ffmpeg ``buffer_size=`` argument on input source, see [2]
- [o] Run pipeline artefacts with the "multiprocessing" module [3]
- [o] Use sequential port numbering
- [o] Add option for controlling "packager" verbosity
- [o] Add runtime reporting and signalling

[1] https://google.github.io/shaka-packager/html/tutorials/encoding.html
[2] https://google.github.io/shaka-packager/html/tutorials/live.html#udp-file-options
[3] https://docs.python.org/3/library/multiprocessing.html
