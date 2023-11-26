from node.host import *


class Server(Host):
    def __init__(self, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        super().__init__(self_ip, self_port)

    def run(self):
        pass

    def listen_for_clients(self):
        # Waiting client for connect
        pass

    def start_file_transfer(self):
        # Handshake & file transfer for all client
        pass

    def file_transfer(self, client_addr: Address):
        # File transfer, server-side, Send file to 1 client
        pass

    def three_way_handshake(self) -> Address:
        # Three-way handshake, server-side, 1 client
        # received = None
        while True:
            # Server start listening for SYN
            self._status = Host.Status.LISTEN
            received: MessageInfo = self._connection.listen_segment(3000)
            if received is not None:
                if received.segment.flags.syn:
                    break

        # Received correct SYN request, status is now SYN-RECV
        self._status = Host.Status.SYN_RECV
        self.init_seq_num()
        dest_addr = received.address

        ack_num = Host.next_seq_num(received.segment.seq_num)
        syn_ack_segment = Segment.syn_ack(self._seq_num, ack_num)
        received = self.send_segment(MessageInfo(syn_ack_segment, dest_addr))

        if received is None:
            pass # TODO handle error

        # SYN-ACK ACK'd, three-way handshake completed
        self._status = Host.Status.ESTABLISHED
        print("Received response from", received.address)

        return dest_addr

if __name__ == '__main__':
    main = Server()
    main.three_way_handshake()
    main.start_file_transfer()
