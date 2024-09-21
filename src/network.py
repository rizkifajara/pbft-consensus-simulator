import random

class Network:
    def __init__(self, nodes):
        self.nodes = nodes

    def broadcast(self, sender, message):
        for node in self.nodes:
            if node != sender:
                if random.random() > 0.1:
                    node.receive_message(message)