from node.host import *


class Client(Host):
    def __init__(self, dest_ip: str, dest_port: int, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        super().__init__(self_ip, self_port)
        self._dest_addr: Address = Address(dest_ip, dest_port)

    def run(self):
        # TODO: find server via broadcast
        pass

    def three_way_handshake(self) -> Address:
        # Three-way handshake, client-side
        self._status = Host.Status.CLOSED
        self.init_seq_num()

        # Client start SYN
        print("Connecting to", self._dest_addr)
        syn_segment = Segment.syn(self._seq_num)

        # SYN segment sent, status is now SYN-SENT
        self._status = Host.Status.SYN_SENT
        received = self.send_segment(MessageInfo(syn_segment, self._dest_addr), max_attempt=4)
        # synchronize acknowledgement number
        self._ack_num = received.segment.seq_num

        # Check server response if SYN-ACK
        if received is not None:
            received_seg = received.segment
            if not (received_seg.flags.syn and received_seg.flags.ack):
                # Received response is incorrect
                pass  # TODO handle incorrect response, need restart

        # SYN ACK'd, status now ESTABLISHED
        self._status = Host.Status.ESTABLISHED
        print("Connection established to", received.address)

        # Send ACK segment for server SYN-ACK, 1 time is enough
        self.send_ack(received.segment.seq_num, self._dest_addr)

        # print(self._seq_num, self._ack_num)
        return received.address

    def listen_file_transfer(self) -> Segment:
        # File transfer, client-side
        pass


if __name__ == '__main__':
    main = Client('127.0.0.1', SERVER_BROADCAST_PORT)
    main.three_way_handshake()
    # main.listen_file_transfer()
