This is to demonstrate an issue with wrapping `maven_install` in a module extension.

* `bazel query @/maven//...` succeeds.
* `REPIN=1 bazel run @unpinned_maven//:pin` succeeds.
* `bazel build //...` fails with:
```
ERROR: no such package '@@[unknown repo 'com_google_guava_failureaccess_1_0_1' requested from @@_main~deps~maven]//file': The repository '@@[unknown repo 'com_google_guava_failureaccess_1_0_1' requested from @@_main~deps~maven]' could not be resolved: No repository visible as '@com_google_guava_failureaccess_1_0_1' from repository '@@_main~deps~maven'
ERROR: /private/var/tmp/_bazel_vinnybod/66f495959bbf72303ba46f2a9dfbb319/external/_main~deps~maven/BUILD:86:8: no such package '@@[unknown repo 'com_google_guava_failureaccess_1_0_1' requested from @@_main~deps~maven]//file': The repository '@@[unknown repo 'com_google_guava_failureaccess_1_0_1' requested from @@_main~deps~maven]' could not be resolved: No repository visible as '@com_google_guava_failureaccess_1_0_1' from repository '@@_main~deps~maven' and referenced by '@@_main~deps~maven//:com_google_guava_failureaccess_1_0_1_extension'
ERROR: Analysis of target '//:HelloWorld' failed; build aborted: Analysis failed
```
