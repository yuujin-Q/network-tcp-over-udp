from lib.address import Address
from lib.segment import Segment
from .host import *


class Client(Host):
    def __init__(self, ip: str, port: int):
        self._connection = Connection(Address())
        self._dest_addr = Address(ip, port)
        self.init_seq_num()
        pass

    def three_way_handshake(self):
        # Three Way Handshake, client-side
        syn_segment = Segment.syn(self._seq_num)
        while True:
            self._connection.send_segment(syn_segment, self._dest_addr)
            received, _ = self._connection.listen_segment()
            if received is not None:
                break
        self._seq_num = received.ack_num

    def listen_file_transfer(self):
        # File transfer, client-side
        pass


if __name__ == '__main__':
    main = Client()
    main.three_way_handshake()
    main.listen_file_transfer()
