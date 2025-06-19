Without `grpc-java`, the `-docs` and `-pom` rules work as expected.
The docs jar generates properly and the pom file contains the protobuf dependencies.

```bash
> bazel build //:hello-world-docs
INFO: Analyzed target //:hello-world-docs (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:hello-world-docs up-to-date:
  bazel-bin/hello-world-docs.jar
INFO: Elapsed time: 0.117s, Critical Path: 0.00s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
```

```bash
> bazel build //:hello-world-pom
INFO: Analyzed target //:hello-world-pom (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:hello-world-pom up-to-date:
  bazel-bin/hello-world-pom.xml
INFO: Elapsed time: 0.123s, Critical Path: 0.00s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action

> cat bazel-bin/hello-world-pom.xml | grep "protobuf" 
            <groupId>com.google.protobuf</groupId>
            <artifactId>protobuf-java-util</artifactId>
            <groupId>com.google.protobuf</groupId>
            <artifactId>protobuf-java</artifactId>
```

Then add `grpc-java` to the MODULE.bazel file. `grpc-java` provides a few `maven.override` entries
[including to protobuf deps](https://github.com/grpc/grpc-java/blob/e6e7bcadafccf908e7bb6f847d86759cfa74fbdb/MODULE.bazel#L91-L204).
Once this is done, the docs target fails to build and the pom file does not contain the protobuf dependencies.

```bash
> bazel build //:hello-world-docs

WARNING: For repository 'com_google_googleapis', the root module requires module version googleapis@0.0.0-20240326-1c8d509c5, but got googleapis@0.0.0-20240819-fe8ba054a in the resolved dependency graph. Please update the version in your MODULE.bazel or set --check_direct_dependencies=off
DEBUG: /private/var/tmp/_bazel_vinnybod/39d3b2a5e001e51d9eace7ba6558c701/external/rules_jvm_external+/private/extensions/maven.bzl:351:18: The maven repository 'maven' has contributions from multiple bzlmod modules, and will be resolved together: ["", "grpc-java", "protobuf"]
INFO: Analyzed target //:hello-world-docs (156 packages loaded, 11124 targets configured).
INFO: From Action hello-world-docs.jar:
javadoc -notimestamp -use -quiet -Xdoclint:-missing -encoding UTF8 -cp bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/errorprone/error_prone_annotations/2.30.0/header_error_prone_annotations-2.30.0.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/code/gson/gson/2.11.0/header_gson-2.11.0.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/code/findbugs/jsr305/3.0.2/processed_jsr305-3.0.2.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/guava/failureaccess/1.0.2/header_failureaccess-1.0.2.jar:bazel-out/darwin_arm64-fastbuild/bin/hello-world-project.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/code/gson/gson/2.11.0/processed_gson-2.11.0.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/org/checkerframework/checker-qual/3.43.0/header_checker-qual-3.43.0.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/errorprone/error_prone_annotations/2.30.0/processed_error_prone_annotations-2.30.0.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/j2objc/j2objc-annotations/3.0.0/header_j2objc-annotations-3.0.0.jar:bazel-out/darwin_arm64-fastbuild/bin/hello-world-project-ijar.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/guava/failureaccess/1.0.2/processed_failureaccess-1.0.2.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/guava/listenablefuture/9999.0-empty-to-avoid-conflict-with-guava/header_listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/guava/listenablefuture/9999.0-empty-to-avoid-conflict-with-guava/processed_listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/guava/guava/33.3.1-android/processed_guava-33.3.1-android.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/org/checkerframework/checker-qual/3.43.0/processed_checker-qual-3.43.0.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/guava/guava/33.3.1-android/header_guava-33.3.1-android.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/code/findbugs/jsr305/3.0.2/header_jsr305-3.0.2.jar:bazel-out/darwin_arm64-fastbuild/bin/external/rules_jvm_external++maven+maven/com/google/j2objc/j2objc-annotations/3.0.0/processed_j2objc-annotations-3.0.0.jar --frames -html5 -d /var/folders/ff/6ltn27kj35558kldkrz7lv_m0000gn/T/output-dir15385993206250624422 /var/folders/ff/6ltn27kj35558kldkrz7lv_m0000gn/T/unpacked-sources13430124949638104741/com/example/HelloWorld.java
javadoc: warning - You have specified to generate frames, by using the --frames option.
The default is currently to not generate frames and the support for 
frames will be removed in a future release.
To suppress this warning, remove the --frames option and avoid the use of frames.
/var/folders/ff/6ltn27kj35558kldkrz7lv_m0000gn/T/unpacked-sources13430124949638104741/com/example/HelloWorld.java:3: error: package com.google.protobuf.util does not exist
import com.google.protobuf.util.JsonFormat;
                               ^
1 error
1 warning

ERROR: /Users/vinnybod/dev/vinnybod/bazel-examples/rules-jvm-external-override-issue/BUILD.bazel:3:12: output 'hello-world-docs.jar' was not created
ERROR: /Users/vinnybod/dev/vinnybod/bazel-examples/rules-jvm-external-override-issue/BUILD.bazel:3:12: output 'hello-world-docs-element-list-dir/element-list' was not created
ERROR: /Users/vinnybod/dev/vinnybod/bazel-examples/rules-jvm-external-override-issue/BUILD.bazel:3:12: Action hello-world-docs.jar failed: not all outputs were created or valid
Target //:hello-world-docs failed to build
Use --verbose_failures to see the command lines of failed build steps.
INFO: Elapsed time: 1.291s, Critical Path: 0.71s
INFO: 5 processes: 953 action cache hit, 1 internal, 4 darwin-sandbox.
ERROR: Build did NOT complete successfully
```

```bash
> bazel build //:hello-world-pom
INFO: Analyzed target //:hello-world-pom (1 packages loaded, 2 targets configured).
INFO: Found 1 target...
Target //:hello-world-pom up-to-date:
  bazel-bin/hello-world-pom.xml
INFO: Elapsed time: 0.198s, Critical Path: 0.00s
INFO: 2 processes: 2 internal.
INFO: Build completed successfully, 2 total actions

> cat bazel-bin/hello-world-pom.xml | grep "protobuf"
```

Interestingly, we can add `excluded_workspaces = {}` to the java_export target, and
the docs begin to generate properly again. But the pom file no longer contains the protobuf dependencies.

```bash
> bazel build //:hello-world-docs
INFO: Analyzed target //:hello-world-docs (1 packages loaded, 4 targets configured).
INFO: Found 1 target...
Target //:hello-world-docs up-to-date:
  bazel-bin/hello-world-docs.jar
INFO: Elapsed time: 5.724s, Critical Path: 5.53s
INFO: 5 processes: 8 action cache hit, 1 internal, 4 darwin-sandbox.
INFO: Build completed successfully, 5 total actions
```

```bash
>  bazel build //:hello-world-pom 
INFO: Analyzed target //:hello-world-pom (0 packages loaded, 1 target configured).
INFO: Found 1 target...
Target //:hello-world-pom up-to-date:
  bazel-bin/hello-world-pom.xml
INFO: Elapsed time: 0.141s, Critical Path: 0.00s
INFO: 1 process: 1 action cache hit, 1 internal.
INFO: Build completed successfully, 1 total action

> cat bazel-bin/hello-world-pom.xml | grep "protobuf"
```

I believe this is a bug in `rules_jvm_external` where the `maven.override` targets generate
aliases to `java_library` targets, but those `java_library` targets lack the tags such as
`maven_coordinates=`.

I don't know what the right solution is here. Should repo owners like `grpc-java` add
`maven_coordinates` tags to their `java_library` targets? Can `rules_jvm_external` add all
the same tags to the `alias` it generates?
