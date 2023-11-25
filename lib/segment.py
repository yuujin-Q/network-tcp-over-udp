import struct
from dataclasses import dataclass

from .constants import *
from .segment_flag import SegmentFlag

CRC_POL = 0b11000000000000101


@dataclass
class Segment:
    seq_num: int
    ack_num: int
    flags: SegmentFlag
    checksum: int
    payload: bytes

    # -- Internal Function --
    def __init__(self, seq_num: int = 0, ack_num: int = 0, flags: bytes = b"\x00"):
        # Initalize segment
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.flags = SegmentFlag(flags)
        self.checksum = 0
        self.payload = b""

    def __str__(self):
        output = ""
        output += f"{'Seq Num':12}\t\t| {self.seq_num}\n"
        output += f"{'Ack Num':12}\t\t| {self.ack_num}\n"
        output += f"{'Flag SYN':12}\t\t| {self.flags.syn}\n"
        output += f"{'Flag ACK':12}\t\t| {self.flags.ack}\n"
        output += f"{'Flag FIN':12}\t\t| {self.flags.fin}\n"
        output += f"{'Checksum':24}| {self.checksum}\n"
        output += f"{'MsgSize':24}| {len(self.payload)}\n"
        return output

    @staticmethod
    def syn(seq_num: int) -> 'Segment':
        segment = Segment(seq_num=seq_num)
        segment.flags.set_flags([SYN_FLAG])

        return segment

    @staticmethod
    def ack(seq_num: int, ack_num: int, payload: bytes = b"") -> 'Segment':
        segment = Segment(seq_num=seq_num, ack_num=ack_num)
        segment.flags.set_flags([ACK_FLAG])
        segment.payload = payload

        return segment

    @staticmethod
    def syn_ack(seq_num: int, ack_num: int) -> 'Segment':
        segment = Segment(seq_num=seq_num, ack_num=ack_num)
        segment.flags.set_flags([SYN_FLAG, ACK_FLAG])

        return segment

    @staticmethod
    def fin(seq_num: int) -> 'Segment':
        segment = Segment(seq_num=seq_num)
        segment.flags.set_flags([FIN_FLAG])

        return segment

    @staticmethod
    def fin_ack(seq_num: int, ack_num: int) -> 'Segment':
        segment = Segment(seq_num=seq_num, ack_num=ack_num)
        segment.flags.set_flags([ACK_FLAG, FIN_FLAG])

        return segment

    def __calculate_checksum(self) -> int:
        # CRC-16/CCITT-FALSE
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

    def is_valid_checksum(self) -> bool:
        return self.checksum == self.__calculate_checksum()

    @staticmethod
    def parse_from_bytes(data: bytes) -> 'Segment':
        seq_num = struct.unpack('I', data[0:4])[0]
        ack_num = struct.unpack('I', data[4:8])[0]
        flags = data[8:9]
        checksum = struct.unpack('H', data[10:12])[0]

        payload = data[12:]

        segment = Segment(seq_num, ack_num, flags)
        segment.checksum = checksum
        segment.payload = payload

        return segment

    @staticmethod
    def convert_to_byte(segment: 'Segment') -> bytes:
        data = b""
        data += struct.pack('II', segment.seq_num, segment.ack_num)
        data += segment.flags.get_flag_bytes()
        data += struct.pack('x')
        data += struct.pack('H', segment.checksum)
        data += segment.payload

        return data

# segment = Segment(seq_num=0, ack_num=1)
# segment.payload = b"bsjdasdjahd testtt"
# print(segment)
# print(segment.payload)
# segment_byte = Segment.convert_to_byte(segment)
# print("")
# print(segment_byte)

# segment2 = Segment.parse_from_bytes(segment_byte)
# print(segment2)
# print(segment2.payload)

# print("segment")
# print(segment)

# syn = segment.syn(segment.seq_num)
# print("syn")
# print(syn)

# ack = segment.ack(segment.seq_num, segment.ack_num)
# print("ack")
# print(ack)

# syn_ack = segment.syn_ack(segment.seq_num, segment.ack_num)
# print("syn_ack")
# print(syn_ack)

# fin = segment.fin(segment.seq_num)
# print("syn")
# print(fin)

# fin_ack = segment.fin_ack(segment.seq_num, segment.ack_num)
# print("fin_ack")
# print(fin_ack)
