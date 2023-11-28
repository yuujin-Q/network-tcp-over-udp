import socket as sc
from dataclasses import dataclass
from socket import socket

from lib.address import Address
from lib.constants import *
from lib.logger import Logger
from lib.messageinfo import MessageInfo
from lib.segment import Segment


@dataclass
class Connection:
    __addr: Address
    __socket: socket

    def __init__(self, addr: Address):
        # Init UDP socket

        # create socket
        self.__socket = socket(sc.AF_INET, sc.SOCK_DGRAM)
        self.__socket.bind(addr.get_address_data())
        new_addr = self.__socket.getsockname()
        self.__addr = Address(new_addr[0], new_addr[1])

    def get_addr(self) -> Address:
        return self.__addr

    def send_segment(self, message: MessageInfo) -> None:
        # Send single segment into destination
        segment = message.segment
        dest = message.address
        self.__socket.sendto(Segment.convert_to_byte(segment), dest.get_address_data())

    def listen_segment(self, timeout: float | None = 0.200) -> MessageInfo | None:
        # Listen single UDP datagram within timeout and convert into segment

        try:
            self.__socket.settimeout(timeout)
            segment_bytes, address = self.__socket.recvfrom(SEGMENT_SIZE)
            parsed_segment = Segment.parse_from_bytes(segment_bytes)

            Logger.connection_log(self.get_addr(), f'Received segment from address {address}', segment=parsed_segment)

            return MessageInfo(parsed_segment, Address(address[0], address[1]))
        except TimeoutError:
            # TODO: log format
            print('Timeout Error')
            return None

    def close_socket(self) -> None:
        # Release UDP socket
        self.__socket.close()
