#!/usr/bin/env python3
import os
import socket
from socketserver import StreamRequestHandler, ThreadingMixIn, UnixStreamServer

SOCKET_PATH = "/run/ipc/ffi_server.socket"

LISTEN_FDS = int(os.environ.get("LISTEN_FDS", 0))
LISTEN_PID = os.environ.get("LISTEN_PID", None) or os.getpid()


def systemd_print(*values):
    import sys

    print(*values)
    sys.stdout.flush()


class Handler(StreamRequestHandler):
    def handle(self):
        while True:
            msg = self.rfile.readline().strip()
            if msg:
                systemd_print(f"Received from client: {msg.decode()}")
            else:
                return


class ThreadedUnixStreamServer(ThreadingMixIn, UnixStreamServer):
    SYSTEMD_FIRST_SOCKET_FD = 3

    def __init__(self, server_address, handler_cls, bind_and_activate=True):
        systemd_print("LISTEN_FDS:", LISTEN_FDS)
        systemd_print("LISTEN_PID:", LISTEN_PID)
        if LISTEN_PID == 0:
            super().__init__(server_address, handler_cls, bind_and_activate)
            return

        super().__init__(server_address, handler_cls, bind_and_activate=False)
        self.socket = socket.fromfd(
            self.SYSTEMD_FIRST_SOCKET_FD, self.address_family, self.socket_type
        )
        if bind_and_activate:
            self.server_activate()


if __name__ == "__main__":
    with ThreadedUnixStreamServer(
        SOCKET_PATH, Handler, bind_and_activate=False
    ) as sock:
        sock.serve_forever()
