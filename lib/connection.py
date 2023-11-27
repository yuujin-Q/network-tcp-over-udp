import socket as sc
from dataclasses import dataclass
from socket import socket

from lib.constants import *
from lib.address import Address
from lib.segment import Segment
from lib.messageinfo import MessageInfo


@dataclass
class Connection:
    __addr: Address
    __socket: socket

    def __init__(self, addr: Address):
        # Init UDP socket
        self.__addr = addr

        # create socket
        self.__socket = socket(sc.AF_INET, sc.SOCK_DGRAM)
        self.__socket.bind(self.__addr.get_address_data())

    def send_segment(self, message: MessageInfo) -> None:
        # Send single segment into destination
        segment = message.segment
        dest = message.address
        self.__socket.sendto(Segment.convert_to_byte(segment), dest.get_address_data())

    def listen_segment(self, timeout: float | None = 0.200) -> MessageInfo:
        # Listen single UDP datagram within timeout and convert into segment

        try:
            self.__socket.settimeout(timeout)
            segment, address = self.__socket.recvfrom(SEGMENT_SIZE)

            print(f'Received segment from address {address}')

            return MessageInfo(Segment.parse_from_bytes(segment), Address(address[0], address[1]))
        except TimeoutError:
            # TODO: log format
            print('Timeout Error')

    def close_socket(self) -> None:
        # Release UDP socket
        self.__socket.close()
