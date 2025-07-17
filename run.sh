docker run --rm -v ${PWD}:/work -w /work cgr.dev/chainguard/apko build wolfi-base.yaml wolfi-base:test wolfi-test.tar
docker load <  wolfi-test.tar
docker run -it wolfi-base:test-amd64
