from dataclasses import dataclass
import struct
from .segment_flag import SegmentFlag

@dataclass
class Segment:
    # -- Internal Function --
    def __init__(self):
        # Initalize segment
        pass

    def __str__(self):
        # Optional, override this method for easier print(segmentA)
        output = ""
        output += f"{'Sequence number':24} | {self.sequence}\n"
        return output

    def __calculate_checksum(self) -> int:
        # Calculate checksum here, return checksum result
        pass


    # -- Setter --
    def set_header(self, header : dict):
        pass

    def set_payload(self, payload : bytes):
        pass

    def set_flag(self, flag_list : list):
        pass


    # -- Getter --
    def get_flag(self) -> SegmentFlag:
        pass

    def get_header(self) -> dict:
        pass

    def get_payload(self) -> bytes:
        pass


    # -- Marshalling --
    def set_from_bytes(self, src : bytes):
        # From pure bytes, unpack() and set into python variable
        pass

    def get_bytes(self) -> bytes:
        # Convert this object to pure bytes
        pass


    # -- Checksum --
    def valid_checksum(self) -> bool:
        # Use __calculate_checksum() and check integrity of this object
        pass
