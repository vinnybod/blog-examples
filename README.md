## build

```bash
bazel build //...
```

## error

```bash
> bazel build //...
INFO: Invocation ID: 0e05c78a-fef6-4502-940c-c75835ea8336
INFO: Analyzed 7 targets (40 packages loaded, 387 targets configured).
INFO: From Action uv_lock_model.json:
WARNING: Local package bazel-examples@0.1.0 elided from pycross repo. It can still be referenced directly from the main repo.
ERROR: /private/var/tmp/_bazel_vrose/68b78de74506d282d50202b667210471/external/rules_pycross++lock_file+uv_lock_file_repo/deps/BUILD.bazel:5:8: Building ruamel.yaml.clib-0.2.12.tar.gz failed: (Exit 1): wheel_builder failed: error executing WheelBuild command (from target @@rules_pycross++lock_file+uv_lock_file_repo//deps:_build_ruamel-yaml-clib@0.2.12) bazel-out/darwin_arm64-opt-exec-ST-96a24bde3e0b/bin/external/rules_pycross+/pycross/private/tools/wheel_builder --sdist ... (remaining 13 arguments skipped)

Use --sandbox_debug to see verbose messages from the sandbox and retain the sandbox build root for debugging
/private/var/tmp/_bazel_vrose/68b78de74506d282d50202b667210471/sandbox/darwin-sandbox/10/execroot/_main/bazel-out/darwin_arm64-opt-exec-ST-96a24bde3e0b/bin/external/rules_pycross+/pycross/private/tools/wheel_builder.runfiles/rules_pycross+/pycross/private/tools/wheel_builder.py:394: DeprecationWarning: Python 3.14 will, by default, filter extracted tar archives and reject files or modify their metadata. Use the filter argument to control this behavior.
  f.extractall(sdist_dir)

Traceback (most recent call last):
  File "/private/var/tmp/_bazel_vrose/68b78de74506d282d50202b667210471/sandbox/darwin-sandbox/10/execroot/_main/bazel-out/darwin_arm64-opt-exec-ST-96a24bde3e0b/bin/external/rules_pycross+/pycross/private/tools/wheel_builder.runfiles/rules_pycross+/pycross/private/tools/wheel_builder.py", line 668, in build_wheel
    wheel_file = builder.build(
                 ^^^^^^^^^^^^^^
  File "/private/var/tmp/_bazel_vrose/68b78de74506d282d50202b667210471/sandbox/darwin-sandbox/10/execroot/_main/bazel-out/darwin_arm64-opt-exec-ST-96a24bde3e0b/bin/external/rules_pycross+/pycross/private/tools/wheel_builder.runfiles/rules_pycross++pycross+rules_pycross_internal/deps/build@1.0.3/site-packages/build/__init__.py", line 298, in build
    return self._call_backend(f'build_{distribution}', output_directory, config_settings, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/tmp/_bazel_vrose/68b78de74506d282d50202b667210471/sandbox/darwin-sandbox/10/execroot/_main/bazel-out/darwin_arm64-opt-exec-ST-96a24bde3e0b/bin/external/rules_pycross+/pycross/private/tools/wheel_builder.runfiles/rules_pycross++pycross+rules_pycross_internal/deps/build@1.0.3/site-packages/build/__init__.py", line 344, in _call_backend
    with self._handle_backend(hook_name):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/tmp/_bazel_vrose/68b78de74506d282d50202b667210471/execroot/_main/external/rules_python++python+python_3_12_aarch64-apple-darwin/lib/python3.12/contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "/private/var/tmp/_bazel_vrose/68b78de74506d282d50202b667210471/sandbox/darwin-sandbox/10/execroot/_main/bazel-out/darwin_arm64-opt-exec-ST-96a24bde3e0b/bin/external/rules_pycross+/pycross/private/tools/wheel_builder.runfiles/rules_pycross++pycross+rules_pycross_internal/deps/build@1.0.3/site-packages/build/__init__.py", line 354, in _handle_backend
    raise BuildBackendException(
build._exceptions.BuildBackendException: Backend 'setuptools.build_meta' is not available.

ERROR Backend 'setuptools.build_meta' is not available.
Use --verbose_failures to see the command lines of failed build steps.
ERROR: /private/var/tmp/_bazel_vrose/68b78de74506d282d50202b667210471/external/rules_pycross++lock_file+uv_lock_file_repo/deps/BUILD.bazel:5:8 Installing ruamel.yaml.clib-0.2.12.whl failed: (Exit 1): wheel_builder failed: error executing WheelBuild command (from target @@rules_pycross++lock_file+uv_lock_file_repo//deps:_build_ruamel-yaml-clib@0.2.12) bazel-out/darwin_arm64-opt-exec-ST-96a24bde3e0b/bin/external/rules_pycross+/pycross/private/tools/wheel_builder --sdist ... (remaining 13 arguments skipped)

Use --sandbox_debug to see verbose messages from the sandbox and retain the sandbox build root for debugging
INFO: Elapsed time: 4.085s, Critical Path: 2.26s
INFO: 24 processes: 2 action cache hit, 1 disk cache hit, 22 internal, 1 darwin-sandbox.
ERROR: Build did NOT complete successfully
```

## uv initialization

```bash
uv init
uv add ruamel.yaml setuptools wheel
```
