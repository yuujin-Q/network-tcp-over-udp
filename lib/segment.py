import math
import struct

from lib.constants import *
from lib.segment_flag import SegmentFlag

class Segment:
    # seq_num: int
    # ack_num: int
    # flags: SegmentFlag
    # checksum: int
    # payload: bytes

    # -- Internal Function --
    def __init__(self, seq_num: int = 0, ack_num: int = 0, flags: bytes = b"\x00"):
        # Initialize segment
        self.seq_num: int = seq_num
        self.ack_num: int = ack_num
        self.flags: SegmentFlag = SegmentFlag(flags)
        self.checksum: int = 0
        self.payload: bytes = b""

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

    def set_payload(self, data: bytes):
        self.payload = data

    def set_flags(self, flags: list[int]):
        self.flags.set_flags(flags)

    def __calculate_checksum(self) -> int:
        # CRC-16/CCITT-FALSE

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
    
    @staticmethod
    def encode_ecc(payload: bytes) -> bytes:
        data_bits = [int(bit) for byte in payload for bit in format(byte, '08b')]
        print(data_bits)
        r = 0 #banyaknya parity bits
        while 2**r - r - 1 < len(data_bits):
            r += 1

        n = len(data_bits) + r #panjang bit yg diretrun

        print(n)
        hamming_code = [-1] * n #inisiasi hamming code pake nilai -1 semua

        print(hamming_code)
        #ngisi bit data 
        j = 0
        for i in range(1, n+1):
            print(i, j)
            if i & (i - 1) != 0:
            # if math.log(i)%2 != 0: 
                #ngosongin indeks 2^n
                hamming_code[i - 1] = data_bits[j]
                j += 1
            print(hamming_code)

        for i in range(r):
            mask = 1 << i
            parity_bit_position = mask - 1
            parity_bit_value = 0
            for j in range(1, n + 1):
                if j & mask != 0:
                    parity_bit_value += hamming_code[j - 1]
            hamming_code[parity_bit_position] = parity_bit_value%2



        print(hamming_code)
        hamming_bytes = bytes([int(''.join(map(str, hamming_code[i:i+8])), 2) for i in range(0, n, 8)])

        return hamming_bytes

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
# data_bytes_8 = bytes([0b10110100])
# hamming_code_8 = segment.encode_ecc(data_bytes_8)
# print("Original data:", data_bytes_8)
# print("Hamming code:", hamming_code_8)

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
