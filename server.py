from dataclasses import dataclass
import random

from lib.constants import LOOPBACK_ADDR, DEFAULT_PORT
from lib.connection import Address
from lib.connection import Segment
from lib.connection import Connection
from node.serverhandler import ServerHandler


@dataclass
class Server:
    def __init__(self, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        self._connection: ServerHandler = ServerHandler(self_ip, self_port)
        self._clients: dict[Address, int] = dict()
        self._used_ports: set[int] = set()

    def listen(self):
        while True:
            pass

    def redirect(self):
        pass

    def run_handler(self):
        pass


if __name__ == "main":
    # TODO: server main script
    # listens client requests
    # starts server handlers for file transfer
    pass
