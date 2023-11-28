from dataclasses import dataclass

from lib.constants import *


@dataclass
class Address:
    _ip: str
    _port: int

    def __init__(self, ip: str = LOOPBACK_ADDR, port: int = DEFAULT_PORT):
        # Init Address fields
        self._ip = ip
        self._port = port

    def __str__(self):
        return str(f"{self._ip}:{self._port}")

    def __hash__(self):
        return hash((self._ip, self._port))

    def __eq__(self, other):
        return self.get_address_data() == other.get_address_data()

    def __ne__(self, other):
        return not (self == other)

    def get_address_data(self):
        return self._ip, self._port

    def get_ip(self) -> str:
        return self._ip

    def get_port(self) -> int:
        return self._port
