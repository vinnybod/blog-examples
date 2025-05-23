This is to demonstrate an issue with wrapping `maven_install` in a module extension.

* `bazel query @maven//...` succeeds.
* 
* `REPIN=1 bazel run @unpinned_maven//:pin` succeeds.
* 
* `bazel build //...` fails with:
```
ERROR: no such package '@@[unknown repo 'com_google_guava_failureaccess_1_0_1' requested from @@_main~deps~maven]//file': The repository '@@[unknown repo 'com_google_guava_failureaccess_1_0_1' requested from @@_main~deps~maven]' could not be resolved: No repository visible as '@com_google_guava_failureaccess_1_0_1' from repository '@@_main~deps~maven'
ERROR: /private/var/tmp/_bazel_vinnybod/66f495959bbf72303ba46f2a9dfbb319/external/_main~deps~maven/BUILD:86:8: no such package '@@[unknown repo 'com_google_guava_failureaccess_1_0_1' requested from @@_main~deps~maven]//file': The repository '@@[unknown repo 'com_google_guava_failureaccess_1_0_1' requested from @@_main~deps~maven]' could not be resolved: No repository visible as '@com_google_guava_failureaccess_1_0_1' from repository '@@_main~deps~maven' and referenced by '@@_main~deps~maven//:com_google_guava_failureaccess_1_0_1_extension'
ERROR: Analysis of target '//:HelloWorld' failed; build aborted: Analysis failed
```

* `bazel query '@maven//:com_google_guava_guava_31_1_jre_extension' --output=build`
```
# /private/var/tmp/_bazel_vinnybod/66f495959bbf72303ba46f2a9dfbb319/external/_main~deps~maven/BUILD:119:8
genrule(
  name = "com_google_guava_guava_31_1_jre_extension",
  visibility = ["//visibility:public"],
  srcs = ["@@[unknown repo 'com_google_guava_guava_31_1_jre' requested from @@_main~deps~maven]//file:file"],
  outs = ["@maven//:com/google/guava/guava/31.1-jre/guava-31.1-jre.jar"],
  cmd = "cp $< $@",
)
```
Note the `@@[unknown repo`

When generated properly it should look like;
```
# /private/var/tmp/_bazel_vinnybod/66f495959bbf72303ba46f2a9dfbb319/external/rules_jvm_external~~maven~maven/BUILD:115:8
genrule(
  name = "com_google_guava_guava_31_1_jre_extension",
  visibility = ["//visibility:public"],
  srcs = ["@@rules_jvm_external~~maven~com_google_guava_guava_31_1_jre//file:file"],
  outs = ["@maven//:com/google/guava/guava/31.1-jre/guava-31.1-jre.jar"],
  cmd = "cp $< $@",
)
```