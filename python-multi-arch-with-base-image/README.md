This example demonstrates:

1. Building a multi-architecture Docker image using a base image that is pulled using `oci.pull`
2. Building a second multi-architecture Docker image using the first image as a base image

Build the first image and make sure it can run:
```shell
➜ bazel run //python-multi-arch-with-base-image/base-image:load
INFO: Analyzed target //python-multi-arch-with-base-image/base-image:load (1 packages loaded, 8 targets configured).
INFO: Found 1 target...
Target //python-multi-arch-with-base-image/base-image:load up-to-date:
  bazel-bin/python-multi-arch-with-base-image/base-image/load.sh
INFO: Elapsed time: 0.109s, Critical Path: 0.00s
INFO: 1 process: 15 action cache hit, 1 internal.
INFO: Build completed successfully, 1 total action
INFO: Running command line: bazel-bin/python-multi-arch-with-base-image/base-image/load.sh
Loaded image: vinnybod/base-image:latest

➜ docker run vinnybod/base-image:latest
This is rules_oci!
```

Build the second image and make sure it can run:
```shell
➜  bazel-examples git:(main) ✗ bazel run //python-multi-arch-with-base-image:load
INFO: Analyzed target //python-multi-arch-with-base-image:load (1 packages loaded, 31 targets configured).
INFO: Found 1 target...
Target //python-multi-arch-with-base-image:load up-to-date:
  bazel-bin/python-multi-arch-with-base-image/load.sh
INFO: Elapsed time: 0.441s, Critical Path: 0.19s
INFO: 3 processes: 64 action cache hit, 3 internal.
INFO: Build completed successfully, 3 total actions
INFO: Running command line: bazel-bin/python-multi-arch-with-base-image/load.sh
Loaded image: vinnybod/py-image:latest
➜  bazel-examples git:(main) ✗ docker run vinnybod/py-image:latest
Hello, World!
```

Attempt to run scapy in the second image:
```shell
➜  bazel run //python-multi-arch-with-base-image:load
INFO: Analyzed target //python-multi-arch-with-base-image:load (1 packages loaded, 31 targets configured).
INFO: Found 1 target...
Target //python-multi-arch-with-base-image:load up-to-date:
  bazel-bin/python-multi-arch-with-base-image/load.sh
INFO: Elapsed time: 0.441s, Critical Path: 0.19s
INFO: 3 processes: 64 action cache hit, 3 internal.
INFO: Build completed successfully, 3 total actions
INFO: Running command line: bazel-bin/python-multi-arch-with-base-image/load.sh
Loaded image: vinnybod/py-image:latest
➜  docker run vinnybod/py-image:latest
Hello, World!
➜  docker run --entrypoint /bin/bash -it vinnybod/py-image:latest                 
root@0e2383d19976:/# cd /python-multi-arch-with-base-image/
root@0e2383d19976:/python-multi-arch-with-base-image# ./scapy
INFO: Can't open /etc/protocols file
INFO: Can't open /etc/services file
INFO: Can't import PyX. Won't be able to use psdump() or pdfdump().
INFO: Can't import python-cryptography v1.7+. Disabled PKI & TLS crypto-related features.
INFO: Can't import python-cryptography v1.7+. Disabled WEP decryption/encryption. (Dot11)
INFO: Can't import python-cryptography v1.7+. Disabled IPsec encryption/authentication.
WARNING: No alternative Python interpreters found ! Using standard Python shell instead.
INFO: Using the default Python shell: History is disabled.
                                      
                     aSPY//YASa       
             apyyyyCY//////////YCa       |
            sY//////YSpcs  scpCY//Pp     | Welcome to Scapy
 ayp ayyyyyyySCP//Pp           syY//C    | Version 2.6.1
 AYAsAYYYYYYYY///Ps              cY//S   |
         pCCCCY//p          cSSps y//Y   | https://github.com/secdev/scapy
         SPPPP///a          pP///AC//Y   |
              A//A            cyP////C   | Have fun!
              p///Ac            sC///a   |
              P////YCpc           A//A   | I'll be back.
       scccccp///pSP///p          p//Y   |                     -- Python 2
      sY/////////y  caa           S//P   |
       cayCyayP//Ya              pY/Ya
        sY/PsY////YCc          aC//Yp 
         sc  sccaCY//PCypaapyCP//YSs  
                  spCPY//////YPSps    
                       ccaacs         
                                      
[34m[1m>>> [0m
```

## Issues

* The Dockerfile version has proper ANSI processing
* The Bazel version shows `[34m[1m>>> [0m`
