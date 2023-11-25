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
        bytes = self.payload
        crc16 = 0xFFFF

        for byte in bytes:
            byte_calc = byte
            print(byte_calc)
            for i in range(8):
                msb_crc = (crc16 & 0x8000) >> 8
                msb_byte = byte_calc & 0x80

                xor = (msb_byte ^ msb_crc)
                print(xor)
                if(xor != 0):
                    crc16 = crc16 ^ 0x1021
                
                byte_calc = (byte_calc << 1) & 0xFF

        return (crc16 & 0xFFFF)
    
    def update_checksum(self) -> None:
        self.checksum = self.__calculate_checksum()
        

    def is_valid_checksum(self) ->bool:
        return (self.checksum == self.__calculate_checksum())

