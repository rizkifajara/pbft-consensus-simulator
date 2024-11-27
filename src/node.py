from abc import ABC, abstractmethod
from .message import Message


class Node(ABC):
    @classmethod
    @abstractmethod
    def handle_message(self, msg: Message):
        pass

    @classmethod
    def get_node_id(self) -> int:
        pass

    @classmethod
    def set_network(self, network):
        pass

    @classmethod
    @abstractmethod
    def timer_expired(self):
        pass

    @classmethod
    @abstractmethod
    def is_decided(self) -> bool:
        pass

    @classmethod
    @abstractmethod
    def debug(self, log: str):
        pass


class FaultyNode:
    """
    A FaultyNode is a node that can't process incoming messages; it is likely offline.
    """

    def get_node_id(self) -> int:
        return -1

    def handle_message(self, msg: Message):
        return

    def set_network(self, network):
        return

    def is_decided(self) -> bool:
        return False

    def timer_expired(self):
        return

    def debug(self, log: str):
        return
