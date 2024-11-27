from .message import Message
from .node import Node
import random
from typing import List


class Network:
    def __init__(self, nodes: List[Node], delivery_threshold: float):
        self.message_log = []
        self.nodes = nodes
        self.num_msgs = 0
        self.delivery_threshold = delivery_threshold

    def broadcast(self, msg: Message):
        self.message_log.append(msg)

    def dispatch(self):
        for msg in self.message_log:
            for node in self.nodes:
                if node.get_node_id() != msg.sender:
                    rnd = random.random()
                    if rnd > self.delivery_threshold:
                        self.num_msgs += 1
                        node.handle_message(msg)
                    else:
                        node.debug(f"message dropped: {msg}")

        self.message_log.clear()
