import socket
from dataclasses import dataclass
from socket import socket

from .constants import *
from .segment import Segment

@dataclass
class Connection:
    __host: str
    __port: int
    __socket: socket

    def __init__(self, host: str = SELF_IP_ADDR, port: int = DEFAULT_PORT):
        # Init UDP socket
        self.__host = host
        self.__port = port

        # create socket
        self.__socket = socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((host, port))

    def send_segment(self, msg: Segment, dest: (str, int)) -> None:
        # Send single segment into destination
        self.__socket.sendto(msg, dest)

    def listen_segment(self, timeout: float = 0.200) -> Segment:
        # Listen single UDP datagram within timeout and convert into segment
        self.__socket.settimeout(timeout)
        # TO-DO implement listen single segment
        pass

    def close_socket(self) -> None:
        # Release UDP socket
        pass
