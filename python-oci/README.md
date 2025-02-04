The goal is to add some list of 3rd party python dependencies to an oci image's
python environment.

I created an "empty" `main.py` `py_binary` with a dependency on `scapy`.
I passed that binary into `py_image_layers`, and the output of that into `oci_image`.


When running the `./main` binary on the image, it does have access to the correct
dependencies and venv.
```shell
➜  bazel run //python-oci:load                                   
INFO: Analyzed target //python-oci:load (1 packages loaded, 18 targets configured).
INFO: Found 1 target...
Target //python-oci:load up-to-date:
  bazel-bin/python-oci/load.sh
INFO: Elapsed time: 3.152s, Critical Path: 2.93s
INFO: 8 processes: 23 action cache hit, 2 internal, 6 darwin-sandbox.
INFO: Build completed successfully, 8 total actions
INFO: Running command line: bazel-bin/python-oci/load.sh
6ab402e3bda1: Loading layer [==================================================>]  20.36MB/20.36MB
70be3e9244bb: Loading layer [==================================================>]  1.108MB/1.108MB
The image vinnybod/py-image:latest already exists, renaming the old one with ID sha256:ce6c22baa3c1a546ca7a51b3f1f98f8246cb017e868574a02f8e8f25188fc32a to empty string
Loaded image: vinnybod/py-image:latest
➜  docker run -it vinnybod/py-image:latest
root@242c46aafb7e:/# cd python-oci/
root@242c46aafb7e:/python-oci# ./main
Hello, World!
>>> import scapy
>>> 
```

# Open Questions

* Is it possible to source the venv without running the `main` script?
* Is it possible to symlink the venv `python` onto the path at the time the image is created?