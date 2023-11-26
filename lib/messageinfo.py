from dataclasses import dataclass

from lib.address import Address
from lib.segment import Segment


@dataclass
class MessageInfo:
    def __init__(self, segment: Segment, address: Address):
        self.segment: Segment = segment
        self.address: Address = address
