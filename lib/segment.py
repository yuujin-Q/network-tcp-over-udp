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
        #CRC-16/CCITT-FALSE
        CRC_XOR_INIT = 0xFFFF  
        CRC_XOR_OUT = 0x0000 
        CRC_POLY = 0x1021

        data = self.payload
        reg = CRC_XOR_INIT
        for byte in data:
            # reflect in
            for i in range(8):
                msb = reg & 0x8000
                if byte & (0x80 >> i):
                    msb ^= 0x8000
                reg <<= 1
                if msb:
                    reg ^= CRC_POLY
            reg &= 0xFFFF
        return reg ^ CRC_XOR_OUT
    
    def update_checksum(self) -> None:
        self.checksum = self.__calculate_checksum()
        

    def is_valid_checksum(self) ->bool:
        return (self.checksum == self.__calculate_checksum())

segment = Segment(payload=b"hello world")
segment.update_checksum()
print(segment.checksum)