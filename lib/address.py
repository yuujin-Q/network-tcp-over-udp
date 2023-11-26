from dataclasses import dataclass
from lib.constants import *


@dataclass
class Address:
    __ip: str
    __port: int

    def __init__(self, ip: str = LOOPBACK_ADDR, port: int = DEFAULT_PORT):
        # Init Address fields
        self.__ip = ip
        self.__port = port

    def get_address_data(self):
        return self.__ip, self.__port

    def get_ip(self) -> str:
        return self.__ip

    def get_port(self) -> int:
        return self.__port
