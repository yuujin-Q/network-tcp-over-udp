import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

from lib.messageinfo import MessageInfo


@dataclass
class Host(ABC):
    class Status:
        (CLOSED,
         LISTEN,
         SYN_SENT,
         SYN_RECV,
         ESTABLISHED) = range(5)

    MAX_SEQ_NUM = 4294967295

    # _connection: Connection
    # _state: int
    # _seq_num: int

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def send_segment(self, message: MessageInfo) -> MessageInfo:
        pass

    def init_seq_num(self):
        self._seq_num = random.randint(0, Host.MAX_SEQ_NUM)

    @staticmethod
    def next_seq_num(num: int):
        if num == Host.MAX_SEQ_NUM:
            return 0
        else:
            return num + 1
