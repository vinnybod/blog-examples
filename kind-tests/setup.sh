./create_kind_cluster.sh

kubectl create namespace mynamespace
bazel run //kind-tests:mynamespace.apply
