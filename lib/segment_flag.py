from dataclasses import dataclass
import struct

from .constants import *

@dataclass
class SegmentFlag:
    ack: bool
    syn: bool
    fin: bool

    def __init__(self, flag: bytes = b'\x00'):
        # Init flag variable from flag byte
        int_flag: int = struct.unpack(f"{ENDIAN_SPECIFIER}b", flag)[0]
        self.ack = bool(int_flag & ACK_FLAG)
        self.syn = bool(int_flag & SYN_FLAG)
        self.fin = bool(int_flag & FIN_FLAG)

    def set_flags(self, flags: list[int]):
        int_flag: int = 0
        for flag in flags:
            int_flag |= flag

        self.ack = bool(int_flag & ACK_FLAG)
        self.syn = bool(int_flag & SYN_FLAG)
        self.fin = bool(int_flag & FIN_FLAG)

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
