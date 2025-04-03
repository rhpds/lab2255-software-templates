#!/usr/bin/env python3
import datetime
import os
import socket
import sys
import time

import psutil

PROCESS = psutil.Process(os.getpid())
PROCESS_CREATION_TIME = datetime.datetime.now().strftime("%X")

SOCKET_PATH = "/run/ipc/ffi_server.socket"

MiB = 1024**2
MEM_CHUNKS = []


class MemoryDump:
    def __init__(self):
        mem = psutil.virtual_memory()
        self.vms = PROCESS.memory_info().vms / MiB
        self.total = mem.total / MiB
        self.available = mem.available / MiB
        self.used = mem.used / MiB
        self.free = mem.free / MiB
        self.percent = mem.percent

    def __str__(self) -> str:
        return (
            f"MemoryDump ({PROCESS_CREATION_TIME}): "
            f"virtual = {self.vms}, total = {self.total}, "
            f"available = {self.available}, used = {self.used}, "
            f"free = {self.free}, percent = {self.percent}"
        )

    def to_bytes(self) -> bytes:
        return self.__str__().encode()


def consume_memory_chunk(chunk_size):
    MEM_CHUNKS.append(" " * chunk_size)


def send_loop():
    chunk_size_mib = 1
    print("Initiating:", MemoryDump())
    sys.stdout.flush()
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        print("Connecting to:", SOCKET_PATH)
        sys.stdout.flush()
        sock.connect(SOCKET_PATH)

        while True:
            try:
                consume_memory_chunk(chunk_size_mib * MiB)
            except MemoryError:
                # A safeguard, in case QM policy failed to close the service.
                MEM_CHUNKS.clear()
                chunk_size_mib = 1
                continue
            print(f"Sending data (allocated {len(MEM_CHUNKS)} chunks)")
            sys.stdout.flush()
            sock.sendall(MemoryDump().to_bytes())
            chunk_size_mib += 1
            time.sleep(1)


if __name__ == "__main__":
    while True:
        try:
            send_loop()
        except OSError as e:
            print("Connection failed:", e)
            print("Retrying")
            sys.stdout.flush()
            time.sleep(5)
