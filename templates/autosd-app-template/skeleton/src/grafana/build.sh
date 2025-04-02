#!/bin/bash

# Requires: podman-compose installed

podman pull grafana/grafana:11.3.1

podman-compose up
