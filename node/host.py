import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

from lib.address import Address
from lib.connection import Connection
from lib.constants import LOOPBACK_ADDR, DEFAULT_PORT, DEFAULT_ATTEMPT
from lib.messageinfo import MessageInfo
from lib.segment import Segment


@dataclass
class Host(ABC):
    class Status:
        (CLOSED,
         LISTEN,
         SYN_SENT,
         SYN_RECV,
         ESTABLISHED) = range(5)

    MAX_SEQ_NUM = 4294967295

    # _connection: Connection
    # _state: int
    # _seq_num: int
    def __init__(self, self_ip: str = LOOPBACK_ADDR, self_port: int = DEFAULT_PORT):
        self._connection: Connection = Connection(Address(self_ip, self_port))
        self._seq_num: int = 0
        self._status: int = Host.Status.CLOSED

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def three_way_handshake(self) -> Address:
        pass

    def send_segment(self,
                     message: MessageInfo,
                     max_attempt: int = DEFAULT_ATTEMPT,
                     ignore_ack: bool = False) -> MessageInfo | None:

        next_seq_num = Host.next_seq_num(self._seq_num)
        received: MessageInfo | None = None
        for _ in range(max_attempt):
            self._connection.send_segment(message)
            received = self._connection.listen_segment()

            if received is not None:
                received_segment = received.segment
                if received_segment.ack_num == next_seq_num or ignore_ack:
                    break

            # print(f"{i} Segment ACK not received, reattempting...")

        if received is None:
            return None

        self._seq_num = next_seq_num
        return received

    def send_ack(self, recv_seq_num: int, dest_addr: Address) -> None:
        # An ACK segment, if carrying no data, consumes no sequence number.
        ack_num = Host.next_seq_num(recv_seq_num)
        ack_segment = Segment.ack(self._seq_num, ack_num)
        self._connection.send_segment(MessageInfo(ack_segment, dest_addr))

    def init_seq_num(self):
        self._seq_num = random.randint(0, Host.MAX_SEQ_NUM)

    # Go Back N ARQ
    def start_receiver_transfer(self):
        # go back-n receiver process

        # TODO: receiver
        # while not FIN:
        #   listen
        #       if receive: send ack

        # reassemble fragments

        pass

    def start_sender_transfer(self):
        # go back-n sender process

        # TODO: sender process
        # fragment frame
        # for each n fragment, send
        #   listen
        #       if ack received for fragment x, increment window start +1, prepare send for fragment-(x+n)
        #       else, resend from x to x+n

        pass

    @staticmethod
    def next_seq_num(num: int):
        if num == Host.MAX_SEQ_NUM:
            return 0
        else:
            return num + 1
