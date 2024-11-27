import time
from .message import Message
from .network import Network
from .node import Node

d_NULL = 0


class PBFTNode(Node):
    def __init__(self, node_id: int, N: int, f: int, disable_logs: bool):
        self.node_id = node_id
        self.pre_prepared = None
        self.prepared = {}
        self.committed = {}
        self.view_changes = {}
        self.N = N
        self.f = f
        self.decided_value = None
        self.phase = "IDLE"
        self.view = 0
        self.primary = 0
        self.disable_logs = disable_logs

    def get_node_id(self) -> int:
        return self.node_id

    def set_network(self, network: Network):
        self.network = network

    def is_decided(self):
        return self.phase == "DECIDED"

    def handle_message(self, msg: Message):
        if msg.view != self.view:
            return

        match msg.msg_type:
            case "<<REQUEST>>":
                self.handle_request(msg)
            case "<<PRE-PREPARE>>":
                self.handle_pre_prepare(msg)
            case "<<PREPARE>>":
                self.handle_prepare(msg)
            case "<<COMMIT>>":
                self.handle_commit(msg)
            case "<<REPLY>>":
                self.handle_reply(msg)
            case "<<VIEW-CHANGE>>":
                self.handle_view_change(msg)
            case "<<NEW-VIEW>>":
                self.handle_new_view(msg)

    def send_message(self, msg: Message):
        self.network.broadcast(msg)
        self.handle_message(msg)
        self.debug(f"sent message {msg}")

    def handle_request(self, msg: Message):
        if self.phase == "IDLE":
            self.phase = "PRE-PREPARE"
            self.debug(f"moved to PRE-PREPARE phase")

            if self.node_id == self.primary:
                pre_prepare_msg = Message(
                    self.node_id,
                    msg.value,  ## The client request message
                    self.view,
                    "<<PRE-PREPARE>>",
                )
                self.send_message(pre_prepare_msg)

    def handle_pre_prepare(self, msg: Message):
        if self.phase == "PRE-PREPARE":
            self.phase = "PREPARE"
            self.pre_prepared = msg
            self.debug(f"moved to PREPARE phase")

            prepare_msg = Message(self.node_id, msg.value, self.view, "<<PREPARE>>")
            self.send_message(prepare_msg)

    def handle_prepare(self, msg: Message):
        if self.phase == "PREPARE":
            self.prepared[msg.sender] = msg
            if len(self.prepared) >= (2 * self.f) + 1:
                self.phase = "COMMIT"
                self.debug(f"moved to COMMIT phase")

                commit_msg = Message(self.node_id, msg.value, self.view, "<<COMMIT>>")
                self.send_message(commit_msg)

    def handle_commit(self, msg: Message):
        if self.phase == "COMMIT":
            self.committed[msg.sender] = msg
            if len(self.committed) >= (2 * self.f) + 1:
                self.phase = "DECIDED"
                self.decided_value = msg.value
                self.debug(f"DECIDED on value: {self.decided_value}")

                reply_msg = Message(self.node_id, msg.value, self.view, "<<REPLY>>")
                self.send_message(reply_msg)

    def handle_reply(self, msg: Message):
        # Reply messages are considered as checkpointing messages.
        # Any replica can make a decision upon receiving a valid Reply message,
        # even if the local log does not have enough votes.
        self.phase = "DECIDED"
        self.decided_value = msg.value

    def timer_expired(self):
        self.request_view_change()

    def request_view_change(self):
        self.phase = "VIEW-CHANGE"
        self.debug(f"moved to VIEW-CHANGE phase")

        # For simplicity, we assume the consensus starts fresh,
        # so there are no checkpoints before this level.
        # This means the C set is empty, and P contains the prepared messages of m, if any.
        # While this simplification helps here, real implementations require checkpointing
        # to ensure the safety of the protocol.

        pre_prepared_msg = None
        prepared_msgs = set()
        if len(self.prepared) >= (2 * self.f) + 1:
            pre_prepared_msg = self.pre_prepared
            prepared_msgs = self.pre_prepared

        P = (pre_prepared_msg, prepared_msgs)
        view_change_msg = Message(self.node_id, None, self.view, "<<VIEW-CHANGE>>", P)
        self.send_message(view_change_msg)

        self.debug(f"requested view change to view {self.view + 1}")

    def handle_view_change(self, msg: Message):
        if self.phase == "VIEW-CHANGE":
            if self.node_id == (self.primary + 1) % self.N:
                self.view_changes[msg.sender] = msg
                if len(self.view_changes) >= (2 * self.f) + 1:
                    self.phase = "NEW-VIEW"
                    self.debug(f"moved to NEW-VIEW phase")

                    V = set()  # V is a set of view-change messages
                    O = set()  # O is a set of pre-prepare messages

                    V = self.view_changes

                    next_pre_prepared_value = d_NULL
                    for vc in self.view_changes.values():
                        if vc.data[0] is not None:
                            next_pre_prepared_value = vc.data[0].value
                            break

                    pre_prepared_msg = Message(
                        self.node_id,
                        next_pre_prepared_value,
                        self.view + 1,
                        "<<PRE-PREPARE>>",
                    )

                    O.add(pre_prepared_msg)

                    new_view_msg = Message(
                        self.node_id,
                        None,
                        self.view,
                        "<<NEW-VIEW>>",
                        (V, O),
                    )
                    self.send_message(new_view_msg)

            else:
                self.phase = "NEW-VIEW"
                self.debug(f"moved to NEW-VIEW phase")

    def handle_new_view(self, msg: Message):
        if self.phase == "NEW-VIEW":
            O = msg.data[1]

            for pre_prepared_msg in O:
                self.view += 1
                self.prepared = {}
                self.committed = {}
                self.view_changes = {}

                self.phase = "PREPARE"
                self.pre_prepared = msg
                self.debug(f"moved to PREPARE phase")

                prepare_msg = Message(
                    self.node_id, pre_prepared_msg.value, self.view, "<<PREPARE>>"
                )
                self.send_message(prepare_msg)

                break

    def debug(self, log: str):
        if not self.disable_logs:
            print(f"Node {self.node_id}, View {self.view} Phase: {self.phase}: {log}")
