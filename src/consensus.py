import time
from src.message import Message

class PBFTConsensus:
    def __init__(self, node):
        self.node = node
        self.prepared = set()
        self.committed = set()
        self.current_value = None
        self.phase = "IDLE"
        self.view = 0
        self.primary = 0
        self.last_activity = time.time()
        self.view_change_timeout = 10  # in seconds

    def start_consensus(self, value):
        self.current_value = value
        self.phase = "PRE-PREPARE"
        self.prepared.clear()
        self.committed.clear()
        message = Message(self.node.id, "PRE-PREPARE", self.current_value)
        self.node.send_message(message)
        self.handle_pre_prepare(message)
        print(f"Node {self.node.id} started consensus with value: {value}")

    def handle_message(self, message):
        self.last_activity = time.time()
        if message.type == "PRE-PREPARE":
            self.handle_pre_prepare(message)
        elif message.type == "PREPARE":
            self.handle_prepare(message)
        elif message.type == "COMMIT":
            self.handle_commit(message)
        elif message.type == "STATUS":
            self.handle_status(message)

    def handle_pre_prepare(self, message):
        if self.phase == "IDLE" or self.phase == "PRE-PREPARE":
            self.current_value = message.content
            self.phase = "PREPARE"
            prepare_message = Message(self.node.id, "PREPARE", self.current_value)
            self.node.send_message(prepare_message)
            self.prepared.add(self.node.id)
            print(f"Node {self.node.id} moved to PREPARE phase")

    def handle_prepare(self, message):
        if self.phase == "PREPARE" or self.phase == "COMMIT":
            self.prepared.add(message.sender)
            if len(self.prepared) > 2 * (self.node.total_nodes - 3) // 3 and self.phase == "PREPARE":
                self.phase = "COMMIT"
                commit_message = Message(self.node.id, "COMMIT", self.current_value)
                self.node.send_message(commit_message)
                self.committed.add(self.node.id)
                print(f"Node {self.node.id} moved to COMMIT phase")

    def handle_commit(self, message):
        if self.phase == "COMMIT":
            self.committed.add(message.sender)
            if len(self.committed) > (self.node.total_nodes - 3) // 2:
                self.phase = "DECIDED"
                print(f"Node {self.node.id} DECIDED on value: {self.current_value}")

    def check_timeout(self):
        current_time = time.time()
        if current_time - self.last_activity > self.view_change_timeout:
            self.request_view_change()

    def request_view_change(self):
        view_change_request = Message(self.node.id, "VIEW-CHANGE-REQUEST", self.view + 1)
        self.node.send_message(view_change_request)
        print(f"Node {self.node.id} requested view change to view {self.view + 1}")

    def check_consensus_status(self):
        if self.phase == "DECIDED":
            status_message = Message(self.node.id, "STATUS", self.current_value)
            self.node.send_message(status_message)

    def handle_status(self, message):
        if self.phase != "DECIDED":
            self.current_value = message.content
            self.phase = "DECIDED"
            print(f"Node {self.node.id} updated to DECIDED based on status message")

