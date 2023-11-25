from dataclasses import dataclass
import struct

from .constants import ENDIAN_SPECIFIER

# Constants
ACK_FLAG = 0b00010000
SYN_FLAG = 0b00000010
FIN_FLAG = 0b00000001


@dataclass
class SegmentFlag:
    __ack: bool
    __syn: bool
    __fin: bool

    def __init__(self, flag: bytes):
        # Init flag variable from flag byte
        int_flag: int = struct.unpack(f"{ENDIAN_SPECIFIER}b", flag)[0]
        self.__ack = bool(int_flag & ACK_FLAG)
        self.__syn = bool(int_flag & SYN_FLAG)
        self.__fin = bool(int_flag & FIN_FLAG)

    def get_flag_bytes(self) -> bytes:
        # Convert this object to flag in byte form
        int_flag: int = 0
        if self.__ack:
            int_flag |= ACK_FLAG

        if self.__syn:
            int_flag |= SYN_FLAG

        if self.__fin:
            int_flag |= FIN_FLAG

        return struct.pack(f"{ENDIAN_SPECIFIER}b", int_flag)
