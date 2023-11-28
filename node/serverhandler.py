from node.host import *


class ServerHandler(Host):
    def __init__(self, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        super().__init__(self_ip, self_port)

    def run(self):
        self._logger.host_log(f"Running server handler on {self.get_address()}")
        destination: Address = self.three_way_handshake()

        self.start_sender_transfer(destination, self._file_payload)

        self.close_connection()

    def listen_for_client(self) -> Address:
        # Waiting client request for connect
        self._logger.host_log("Listening for connection request")

        return self.three_way_handshake()

    def three_way_handshake(self) -> Address:
        # Three-way handshake, server-side, 1 client
        self._logger.host_log("Listening for Three Way Handshake")

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

        self._logger.host_log(f"Connection request received from {dest_addr}")

        self._ack_num = Host.next_seq_num(received.segment.seq_num)
        syn_ack_segment = Segment.syn_ack(self._seq_num, self._ack_num)

        received = self.send_segment(MessageInfo(syn_ack_segment, dest_addr))

        # SYN-ACK ACK'd, three-way handshake completed
        self._status = Host.Status.ESTABLISHED

        self._logger.host_log(f"Connection established to {received.address}")
        self._logger.host_log("Three Way Handshake Completed")

        return dest_addr


if __name__ == '__main__':
    main = ServerHandler(self_port=SERVER_BROADCAST_PORT)
    dest = main.three_way_handshake()
    with open("img.png", "rb") as img:
        data = img.read()
        main.start_sender_transfer(dest, data)
