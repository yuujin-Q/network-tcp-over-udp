from .host import *

CONNECT_ATTEMPT = 4

class Client(Host):
    def __init__(self, ip: str, port: int):
        self._connection = Connection(Address())
        self._dest_addr = Address(ip, port)
        self._seq_num = 0
        self._status = Host.Status.CLOSED

    def three_way_handshake(self):
        # Three Way Handshake, client-side
        self._status = Host.Status.CLOSED
        self.init_seq_num()
        next_seq_num = Host.next_seq_num(self._seq_num)

        # Client SYN
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
                if received.ack_num == next_seq_num:
                    break
        
        # SYN ACK'd, status now ESTABLISHED
        print("Received response from", self._dest_addr)
        self._status = Host.Status.ESTABLISHED
        # Send ACK segment for server SYN-ACK
        self._seq_num = next_seq_num
        ack_segment = Segment.ack(self._seq_num, received.seq_num + 1)
        self._connection.send_segment(ack_segment, self._dest_addr)



    def listen_file_transfer(self):
        # File transfer, client-side
        pass


if __name__ == '__main__':
    main = Client()
    main.three_way_handshake()
    main.listen_file_transfer()
