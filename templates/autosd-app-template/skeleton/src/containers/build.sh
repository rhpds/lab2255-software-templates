#!/bin/bash

FEDORA_VERSION=40

# Build "ffi_client" container
podman build -t localhost/ffi_client:latest \
    --build-arg FEDORA_VERSION=$FEDORA_VERSION \
    ffi_client

# Build "ffi_server" container
podman build -t localhost/ffi_server:latest \
    --build-arg FEDORA_VERSION=$FEDORA_VERSION \
    ffi_server

# Build "sysbench" container
podman build -t localhost/sysbench:latest \
    --build-arg FEDORA_VERSION=$FEDORA_VERSION \
    sysbench
