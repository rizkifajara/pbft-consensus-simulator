from src.message import Message
from src.network import Network
from src.node import Node
from typing import List


class Simulator:
    def __init__(self, name: str, nodes: List[Node], f: int, delivery_threshold: float):
        self.f = f
        self.nodes = nodes
        self.network = Network(nodes, delivery_threshold)
        self.name = name

        for node in self.nodes:
            node.set_network(self.network)

    def start(self):
        value = "Hello World!"
        msg = Message(-1, value, 0, "<<REQUEST>>")

        for node in self.nodes:
            node.handle_message(msg)

        while True:
            self.network.dispatch()

            if not self.decided():
                # Use a simple trick to handle the timer in the network:
                # If, for any reason, the network cannot decide on a value,
                # we expire the timer for all nodes in the network.
                # This simulates timer expiration synchronously and ensures
                # the safety of the protocol.
                for node in self.nodes:
                    node.timer_expired()

                self.network.dispatch()

                if not self.decided():
                    print(f"!!! {self.name} CONSENSUS HALTED !!!")
                    return
            else:
                break

        print(f"{self.name} Consensus decided after {self.network.num_msgs} messages")

    def decided(self):
        decided = 0
        for node in self.nodes:
            if node.is_decided():
                decided += 1

        # The network is considered to have decided on a value
        # once at least 2f + 1 nodes have decided on the same value.
        return decided >= (self.f * 2) + 1
