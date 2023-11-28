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

    def __init__(self, addr: Address, enable_ecc: bool = ENABLE_ECC):
        # Init UDP socket

        # create socket
        self.__socket = socket(sc.AF_INET, sc.SOCK_DGRAM)
        self.__socket.bind(addr.get_address_data())
        new_addr = self.__socket.getsockname()
        self.__addr = Address(new_addr[0], new_addr[1])
        self.__ecc_enabled = enable_ecc

    def get_addr(self) -> Address:
        return self.__addr

    def send_segment(self, message: MessageInfo) -> None:
        # Send single segment into destination
        segment = message.segment

        if self.__ecc_enabled:
            # assume that encoded fits in segment size
            segment.payload = Segment.encode_all_payload(segment.payload)

        dest = message.address
        self.__socket.sendto(Segment.convert_to_byte(segment), dest.get_address_data())

        Logger.connection_log(self.get_addr(), f'Sent segment to address {dest}', segment=segment)

    def listen_segment(self, timeout: float | None = 0.200) -> MessageInfo | None:
        # Listen single UDP datagram within timeout and convert into segment

        try:
            self.__socket.settimeout(timeout)
            segment_bytes, address = self.__socket.recvfrom(SEGMENT_SIZE)

            parsed_segment = Segment.parse_from_bytes(segment_bytes)

            if self.__ecc_enabled:
                # assume
                decoded_payload = Segment.decode_all(parsed_segment.payload)
                parsed_segment.payload = decoded_payload

            Logger.connection_log(self.get_addr(),
                                  f'Received segment from address {address}', segment=parsed_segment)

            return MessageInfo(parsed_segment, Address(address[0], address[1]))
        except TimeoutError:
            # TODO: raise exception
            Logger.connection_log(self.get_addr(), 'Connection Timeout')
            return None

    def close_socket(self) -> None:
        # Release UDP socket
        Logger.connection_log(self.get_addr(), 'Terminating Socket')
        self.__socket.close()
