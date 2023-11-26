from node.host import *

CONNECT_ATTEMPT = 4


class Client(Host):
    def send_segment(self, message: MessageInfo) -> MessageInfo:
        pass

    def __init__(self, dest_ip: str, dest_port: int, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        self._connection: Connection = Connection(Address(self_ip, self_port))
        self._dest_addr: Address = Address(dest_ip, dest_port)
        self._seq_num: int = 0
        self._status: int = Host.Status.CLOSED

    def run(self):
        pass

    def three_way_handshake(self):
        # Three-way handshake, client-side
        self._status = Host.Status.CLOSED
        self.init_seq_num()
        next_seq_num = Host.next_seq_num(self._seq_num)

        # Client start SYN
        syn_segment = Segment.syn(self._seq_num)
        received = None
        for _ in range(CONNECT_ATTEMPT):
            print("Connecting to", self._dest_addr)
            self._connection.send_segment(syn_segment, self._dest_addr)
            # SYN segment sent, status is now SYN-SENT
            self._status = Host.Status.SYN_SENT

            # Wait for Server SYN-ACK
            received, _ = self._connection.listen_segment()
            if received is not None:
                if (received.flags.syn and received.flags.ack
                        and received.ack_num == next_seq_num):
                    # Received response is correct
                    break

        # SYN ACK'd, status now ESTABLISHED
        print("Received response from", self._dest_addr)
        self._status = Host.Status.ESTABLISHED
        # Send ACK segment for server SYN-ACK, 1 times is enough
        self._seq_num = next_seq_num
        ack_segment = Segment.ack(self._seq_num, received.seq_num + 1)
        self._connection.send_segment(ack_segment, self._dest_addr)

    def listen_file_transfer(self) -> Segment:
        # File transfer, client-side
        pass


if __name__ == '__main__':
    main = Client('127.0.0.1', DEFAULT_PORT, self_port=9999)
    main.three_way_handshake()
    main.listen_file_transfer()
