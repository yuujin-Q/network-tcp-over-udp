from node.host import *


class ServerHandler(Host):
    def __init__(self, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        super().__init__(self_ip, self_port)

    def run(self):
        # TODO: implement
        pass

    def listen_for_clients(self):
        # Waiting client for connect
        # TODO: implement
        pass

    def three_way_handshake(self) -> Address:
        # Three-way handshake, server-side, 1 client
        # received = None
        while True:
            # Server start listening for SYN
            self._status = Host.Status.LISTEN
            received: MessageInfo = self._connection.listen_segment(None)
            if received is not None:
                if received.segment.flags.syn:
                    break

        # Received correct SYN request, status is now SYN-RECV
        self._status = Host.Status.SYN_RECV
        self.init_seq_num()
        dest_addr = received.address

        print("Connection request received from", dest_addr)

        self._ack_num = Host.next_seq_num(received.segment.seq_num)
        syn_ack_segment = Segment.syn_ack(self._seq_num, self._ack_num)

        received = self.send_segment(MessageInfo(syn_ack_segment, dest_addr))

        # SYN-ACK ACK'd, three-way handshake completed
        self._status = Host.Status.ESTABLISHED
        print("Connection established to", received.address)

        # print(self._seq_num, self._ack_num)
        return dest_addr


if __name__ == '__main__':
    main = ServerHandler(self_port=SERVER_BROADCAST_PORT)
    main.three_way_handshake()
    # main.start_file_transfer()
