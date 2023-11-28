from node.host import *


class Client(Host):
    def __init__(self, dest_ip: str, dest_port: int, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        super().__init__(self_ip, self_port)
        self._dest_addr: Address = Address(dest_ip, dest_port)

    def three_way_handshake(self) -> Address:
        # Three-way handshake, client-side
        self._status = Host.Status.CLOSED
        self.init_seq_num()

        # Client start SYN
        self._logger.host_log(f"Initiating Three Way Handshake with {self._dest_addr}")
        syn_segment = Segment.syn(self._seq_num)

        # SYN segment sent, status is now SYN-SENT
        self._status = Host.Status.SYN_SENT
        received = self.send_segment(MessageInfo(syn_segment, self._dest_addr), WAITING_TIMEOUT)
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
        self._logger.host_log(f"Connection established to {received.address}")

        # Send ACK segment for server SYN-ACK, 1 time is enough
        self.send_ack(received.segment.seq_num, self._dest_addr)

        self._logger.host_log("Three Way Handshake Completed")
        return received.address


if __name__ == '__main__':
    # main = Client('192.168.1.116', SERVER_BROADCAST_PORT, self_ip='192.168.1.63')
    main = Client(LOOPBACK_ADDR, SERVER_BROADCAST_PORT)
    dest = main.three_way_handshake()
    # data = main.start_receiver_transfer(dest)
    # with open("img_dest.mp4", "wb") as img:
    #     img.write(data)
