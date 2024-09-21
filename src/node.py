from src.message import Message
import random

class Node:
    def __init__(self, node_id, total_nodes):
        self.id = node_id
        self.total_nodes = total_nodes
        self.consensus = None
        self.network = None
        self.message_queue = []

    def set_network(self, network):
        self.network = network

    def receive_message(self, message):
        self.message_queue.append(message)

    def send_message(self, message):
        self.network.broadcast(self, message)

    def process_messages(self):
        self.consensus.check_timeout()
        while self.message_queue:
            message = self.message_queue.pop(0)
            self.consensus.handle_message(message)

class ByzantineNode(Node):
    def __init__(self, node_id, total_nodes, byzantine_behavior='random'):
        super().__init__(node_id, total_nodes)
        self.byzantine_behavior = byzantine_behavior

    def send_message(self, message):
        if self.byzantine_behavior == 'random':
            if random.random() < 0.5:
                message.content = self.corrupt_message(message.content)
        elif self.byzantine_behavior == 'silent':
            return
        elif self.byzantine_behavior == 'liar':
            message.content = self.corrupt_message(message.content)
        
        if self.network:
            self.network.broadcast(self, message)

    def corrupt_message(self, content):
        if isinstance(content, str):
            return content[::-1]
        elif isinstance(content, int):
            return content + 1
        return content

    def process_messages(self):
        if self.byzantine_behavior == 'silent':
            return
        elif self.byzantine_behavior == 'liar':
            if random.random() < 0.3:
                if self.consensus.phase == "PREPARE":
                    self.consensus.handle_prepare(Message(self.id, "PREPARE", "Conflicting Value"))
                elif self.consensus.phase == "COMMIT":
                    self.consensus.handle_commit(Message(self.id, "COMMIT", "Conflicting Value"))
            else:
                super().process_messages()
        elif self.byzantine_behavior == 'random':
            if random.random() < 0.5:
                super().process_messages()
