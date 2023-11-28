import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

from lib.address import Address
from lib.connection import Connection
from lib.constants import *
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
        self._ack_num: int | None = None
        self._status: int = Host.Status.CLOSED

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def three_way_handshake(self) -> Address:
        pass

    def send_segment(self,
                     message: MessageInfo,
                     max_attempt: int = DEFAULT_ATTEMPT) -> MessageInfo | None:

        next_seq_num = Host.next_seq_num(self._seq_num)
        received: MessageInfo | None = None
        for _ in range(max_attempt):
            self._connection.send_segment(message)
            received = self._connection.listen_segment()

            print(received)
            if received is not None:
                received_segment = received.segment
                if received_segment.ack_num == next_seq_num:
                    break

            # print(f"{i} Segment ACK not received, reattempting...")

        if received is None:
            return None

        self._seq_num = next_seq_num
        self._ack_num = Host.next_seq_num(received.segment.seq_num)
        return received

    def send_ack(self, recv_seq_num: int, dest_addr: Address) -> None:
        # An ACK segment, if carrying no data, consumes no sequence number.
        self._ack_num = Host.next_seq_num(recv_seq_num)
        ack_segment = Segment.ack(self._seq_num, self._ack_num)
        self._connection.send_segment(MessageInfo(ack_segment, dest_addr))

    def init_seq_num(self):
        self._seq_num = random.randint(0, Host.MAX_SEQ_NUM)

    # Go Back N ARQ
    def start_receiver_transfer(self, src_address: Address) -> bytes:
        # go back-n receiver process

        # payload segment buffer
        payload_segments: list[Segment] = []
        while True:
            # TODO: timeout handling
            # listen for payload fragments

            received = self._connection.listen_segment(1000)
            if received is not None:
                # if EOF received
                if received.segment.flags.fin:
                    break

                if self._ack_num == received.segment.seq_num:
                    # cache payload segment
                    payload_segments.append(received.segment)

                    # reply sender with ACK
                    self.send_ack(received.segment.seq_num, src_address)

        # reassemble payload
        payload = b''
        for segment in payload_segments:
            payload += segment.payload

        return payload

    def start_sender_transfer(self, dest_address: Address, payload: bytes,
                              chunk_size: int = PAYLOAD_SIZE, window_size: int = WINDOW_SIZE):
        # go back-n sender process

        # chunk payload files to chunks
        chunks = [payload[i:i + chunk_size] for i in range(0, len(payload), chunk_size)]

        # prepare segments
        payload_segments: list[Segment] = []
        seq_num_idx = self._seq_num
        for chunk in chunks:
            # create segment for chunk
            chunk_segment = Segment(seq_num=seq_num_idx, ack_num=self._ack_num)
            chunk_segment.set_payload(chunk)

            payload_segments.append(chunk_segment)

            seq_num_idx = Host.next_seq_num(seq_num_idx)
        # TODO: FIN FLAG
        # payload_segments[-1].set_flags(FIN_FLAG)

        # start send
        window_start_index = 0
        max_window_count = len(payload_segments)
        while window_start_index < len(payload_segments):
            # TODO: try catch

            # send segments in window
            # calculate windows size for send
            send_window_size = min(window_size, max_window_count - window_start_index)
            for i in range(send_window_size):
                # send a segment
                self._connection.send_segment(MessageInfo(payload_segments[window_start_index + i], dest_address))

            # assume client ACK sequentially
            # listen for ack
            end_time = time.time() + 2 * DEFAULT_TIMEOUT
            diff = window_start_index
            while time.time() < end_time and diff < window_start_index + send_window_size:
                received_ack_msg = self._connection.listen_segment()

                if received_ack_msg is None:
                    continue

                # check if ACK is within window bounds
                recv_ack_segment = received_ack_msg.segment
                diff = Host.seq_num_diff(recv_ack_segment.ack_num, seq_num_idx)

            # update window start position
            window_start_index = diff

        # send for transfer completed, send FIN
        self.send_fin_segment(dest_address)

    def send_fin_segment(self, dest_address: Address):
        fin_segment = Segment.fin(self._seq_num)
        self._connection.send_segment(MessageInfo(fin_segment, dest_address))

    @staticmethod
    def next_seq_num(num: int):
        if num == Host.MAX_SEQ_NUM:
            return 0
        else:
            return num + 1

    @staticmethod
    def seq_num_diff(upper_num: int, lower_num: int) -> int:
        if upper_num < lower_num:
            return Host.MAX_SEQ_NUM - lower_num + upper_num
        else:
            return upper_num - lower_num
