#!/bin/bash

CONTAINER_BASE="centos:stream9"

# Build all containers
for i in $(ls -1 | grep -v ${0}); do
    echo "Building ${i} ..."
    podman build -t localhost/${i}:latest \
    --build-arg CONTAINER_BASE=$CONTAINER_BASE \
    ${i}
done
