This is to demonstrate an issue with registering a custom toolchain with rules_scala 7.0.0
To run this example, `cd` into the `scala-custom-toolchain` directory.

```bash
bazel build //...
```

To see the build work with the default toolchain,
comment out the `register_toolchain` call in `MODULE.bazel` and
re-enable the `scala_deps.scala()` line.

To see the build fail with the custom toolchain,
comment out the `scala_deps.scala()` line in `MODULE.bazel` and
re-enable the `register_toolchain` line.

```bash
> bazel build //...
ERROR: no such package '@@[unknown repo 'rules_scala_config' requested from @@]//': The repository '@@[unknown repo 'rules_scala_config' requested from @@]' could not be resolved: No repository visible as '@rules_scala_config' from main repository
ERROR: /Users/vinnybod/dev/vinnybod/bazel-examples/scala-custom-toolchain/toolchains/BUILD.bazel:3:22: no such package '@@[unknown repo 'rules_scala_config' requested from @@]//': The repository '@@[unknown repo 'rules_scala_config' requested from @@]' could not be resolved: No repository visible as '@rules_scala_config' from main repository and referenced by '//toolchains:my_toolchain'
ERROR: /Users/vinnybod/dev/vinnybod/bazel-examples/scala-custom-toolchain/BUILD.bazel:3:14: Analysis failed
ERROR: Analysis of target '//:main' failed; build aborted
INFO: Elapsed time: 0.193s, Critical Path: 0.00s
INFO: 1 process: 1 internal.
ERROR: Build did NOT complete successfully
```
