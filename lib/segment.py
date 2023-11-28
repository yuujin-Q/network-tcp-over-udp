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
        # Convert bytes to a list of bits
        data_bits = [int(bit) for byte in payload for bit in format(byte, '08b')]
        data_bits = data_bits[4:8]
        data_bits = data_bits[::-1]
        print(data_bits)

        # Calculate the total number of bits (n)
        n = 7

        # Initialize the encoded data with placeholder values
        hamming_code = [-1] * (n + 1)

        # Fill in the data bits in their correct positions
        j = 0
        for i in range(1, n + 2):
            if i & (i - 1) != 0:  # Skip positions that are powers of 2
                hamming_code[i] = data_bits[j]
                j += 1

        print(hamming_code)
        hamming_code[1] = hamming_code[3] ^ hamming_code[5] ^ hamming_code[7]
        hamming_code[2] = hamming_code[3] ^ hamming_code[6] ^ hamming_code[7]
        hamming_code[4] = hamming_code[5] ^ hamming_code[6] ^ hamming_code[7]

        hamming_code[0] = 0

        # hamming_code = hamming_code[::-1]
        result = [0]
        hamming_code = hamming_code[1:8]
        hamming_code = hamming_code[::-1]
        result += hamming_code

        print(result)
        hamming_bytes = bytearray([int(''.join(map(str, result[i:i + 8])), 2) for i in range(0, n, 8)])

        return hamming_bytes
    
    @staticmethod
    def decode_ecc(encoded: bytes)->bytes:
        data_bits = [int(bit) for byte in encoded for bit in format(byte, '08b')]
        print(data_bits)
        data_bits = data_bits[1:8]
        data_bits = data_bits[::-1]
        
        print(data_bits)
        res = []
        for i in range (0, len(data_bits)):
            if i & (i + 1) != 0:
                res += [data_bits[i]]
            print(res)
        
        res += ([0]*4)

        res = res[::-1]
        print(res)
        return bytearray([int(''.join(map(str, res[i:i+8])), 2) for i in range(0, len(res), 8)])


    @staticmethod
    def detect_and_correct(encoded_data: bytes) -> bytes:
        data_bits = [int(bit) for byte in encoded_data for bit in format(byte, '08b')]
        # print(data_bits)
        data_bits = data_bits[1:8]
        data_bits = data_bits[::-1]

        parity = []
        parity += [data_bits[0] ^ data_bits[2] ^ data_bits[4] ^ data_bits[6]]
        parity += [data_bits[1] ^ data_bits[2] ^ data_bits[5] ^ data_bits[6]]
        parity += [data_bits[3] ^ data_bits[4] ^ data_bits[5] ^ data_bits[6]]

        print(parity)
        err_pos = 0
        for i in range(0, len(parity)):
            if(parity[i] == 1):
                err_pos += 2**i
        
        result = data_bits
        if(err_pos > 0):
            if(result[err_pos-1] == 1):
                result[err_pos-1] = 0
            else:
                result[err_pos-1] = 1
        
        result = result[::-1]
        result = [0] + result

        # print(result)
        return bytearray([int(''.join(map(str, result[i:i+8])), 2) for i in range(0, len(result), 8)])
    




# segment = Segment(seq_num=0, ack_num=1)
# data_bytes_4 = bytearray([0b0001])
# hamming_code_4 = segment.encode_ecc(data_bytes_4)
# print("Hamming code:", hamming_code_4)
# print (segment.detect_and_correct(hamming_code_4))

# print (segment.detect_and_correct([0b0001111]))


# print("Original data:", data_bytes_4)


# decoded = segment.decode_ecc(hamming_code_4)
# print(decoded)



