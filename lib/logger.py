from lib.address import Address
from lib.segment import Segment


class Logger:
    def __init__(self, address: Address):
        self._address = address

    def host_log(self, msg: str, segment: Segment = None):
        Logger.connection_log(self._address, msg, segment)

    @staticmethod
    def _log(msg: str):
        print(msg)

    @staticmethod
    def connection_log(host_address: Address, msg: str, segment: Segment = None):
        log: str = f'[{host_address}]'

        if segment is not None:
            log += f'[SEQ={segment.seq_num}]'
            log += f'[ACK={segment.ack_num}]'
            log += f'[Flags={str(segment.flags)}]'

        log += f' {msg}'

        Logger._log(log)
