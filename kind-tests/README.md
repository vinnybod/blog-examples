Copied from rules_gitops. Stripped down example of running tests on a kind cluster.
Requires kind installed.

```bash
cd kind-tests
./setup.sh
cd ..
bazel test //kind-tests:hello_server_it
```