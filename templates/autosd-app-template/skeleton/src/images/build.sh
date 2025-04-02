#!/usr/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR


image=true
while [[ $# -gt 0 ]]; do
  case $1 in
    --noimage)
      image=false
      shift # past argument
      ;;
  esac
done

set -xe

arch=$(arch)

if [ $image = true ]; then
  automotive-image-builder --verbose \
    --include=/var/lib/containers/storage/ \
    build \
    --distro autosd9 \
    --target qemu \
    --mode package \
    --build-dir=_build \
    --export qcow2 \
    ffi.aib.yml \
    ffi.$arch.qcow2

   u=$USER
   sudo chown $u:$u *.qcow2
fi
