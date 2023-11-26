from node.host import *


class Server(Host):
    def send_segment(self, message: MessageInfo) -> MessageInfo:
        pass

    def __init__(self, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        self._connection: Connection = Connection(Address(self_ip, self_port))
        self._seq_num: int = 0
        self._status: int = Host.Status.CLOSED

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

    def three_way_handshake(self, client_addr: Address):
        # Three-way handshake, server-side, 1 client
        received = None
        while True:
            # Server start listening for SYN
            self._status = Host.Status.LISTEN
            received, _ = self._connection.listen_segment(3000)
            if received is not None:
                if received.flags.syn:
                    break

        # Received correct SYN request, status is now SYN-RECV
        self._status = Host.Status.SYN_RECV
        self.init_seq_num()
        ack_num = Host.next_seq_num(received.seq_num)

        pass


if __name__ == '__main__':
    main = Server()
    main.listen_for_clients()
    main.start_file_transfer()
