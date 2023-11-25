from dataclasses import dataclass
import struct
from .segment_flag import SegmentFlag 
from .constants import *

CRC_POL = 0b11000000000000101

@dataclass
class Segment:
    flags: SegmentFlag
    seq_num: int
    ack_num: int
    checksum: bytes
    payload: bytes

    # -- Internal Function --
    def __init__(self, seq_num: int = 0, ack_num: int = 0,payload: bytes = b""):
        # Initalize segment
        self.flags = SegmentFlag()
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.payload = payload

    def __str__(self):
        # Optional, override this method for easier print(segmentA)
        output = ""
        output += f"{'Sequence number':24} | {self.sequence}\n"
        return output

    @staticmethod
    def syn(seq_num: int) -> 'Segment': 
        segment = Segment(seq_num= seq_num)
        segment.flags.set_flags([SYN_FLAG])

        return segment

    @staticmethod
    def ack(seq_num: int, ack_num: int) -> 'Segment':
        segment = Segment(seq_num= seq_num, ack_num= ack_num)

        segment.flags.set_flags([ACK_FLAG])

        return segment
    
    @staticmethod
    def syn_ack(seq_num: int, ack_num: int) -> 'Segment':
        segment = Segment(seq_num= seq_num, ack_num= ack_num)

        segment.flags.set_flags([SYN_FLAG, ACK_FLAG])

        return segment

    @staticmethod
    def fin(seq_num: int) -> 'Segment':
        segment = Segment(seq_num= seq_num)
        segment.flags.set_flags([FIN_FLAG])

        return segment

    @staticmethod
    def fin_ack(seq_num: int, ack_num: int) -> 'Segment':
        segment = Segment(seq_num= seq_num, ack_num= ack_num)

        segment.flags.set_flags([ACK_FLAG, FIN_FLAG])

        return segment

    def __calculate_checksum(self) -> bytes:
        xor_in = 0xFFFF  # initial value
        xor_out = 0x0000  # final XOR value
        poly = 0x1021  # generator polinom (normal form)

        data = self.payload
        reg = xor_in
        for octet in data:
            # reflect in
            for i in range(8):
                topbit = reg & 0x8000
                if octet & (0x80 >> i):
                    topbit ^= 0x8000
                reg <<= 1
                if topbit:
                    reg ^= poly
            reg &= 0xFFFF
            # reflect out
        return reg ^ xor_out
    
    def update_checksum(self) -> None:
        self.checksum = self.__calculate_checksum()
        

    def is_valid_checksum(self) ->bool:
        return (self.checksum == self.__calculate_checksum())

segment = Segment(payload=b"123456789")
segment.update_checksum()
print(segment.checksum)