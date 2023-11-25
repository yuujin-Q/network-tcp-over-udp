import socket
from dataclasses import dataclass
from socket import socket

from .address import Address
from .constants import *
from .segment import Segment


@dataclass
class Connection:
    __addr: Address
    __socket: socket

    def __init__(self, addr: Address):
        # Init UDP socket
        self.__addr = addr

        # create socket
        self.__socket = socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind(self.__addr.get_address_data())

    def send_segment(self, msg: Segment, dest: Address) -> None:
        # Send single segment into destination
        self.__socket.sendto(msg, dest.get_address_data())

    def listen_segment(self, timeout: float = 0.200) -> Segment:
        # Listen single UDP datagram within timeout and convert into segment

        try:
            self.__socket.settimeout(timeout)
            message, address = self.__socket.recvfrom(SEGMENT_SIZE)

            print(f'Received segment from address {address}')
            return Segment(message)
        except TimeoutError:
            # TODO: log format
            print('Timeout Error')

    def close_socket(self) -> None:
        # Release UDP socket
        self.__socket.close()
