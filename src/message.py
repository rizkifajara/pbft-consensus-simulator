class Message:
    """
    Represents a message broadcast within the network during the consensus protocol.
    For simplicity, message digests and cryptographic signatures are ignored in this implementation.

    Attributes:
        sender (str): The ID of the replica in the network that sends the message.
        value (str): The client message data.
        view (int): The view number of the protocol.
        msg_type (str): The type of the message (e.g., PRE-PREPARE, PREPARE, COMMIT, etc.).
        data (any = None): Arbitrary additional data associated with the message; can be None.
    """

    def __init__(
        self, sender: str, value: any, view: int, msg_type: str, data: any = None
    ):
        self.sender = sender
        self.value = value
        self.msg_type = msg_type
        self.view = view
        self.data = data

    def __repr__(self):
        return f"(Sender={self.sender}, View={self.view} Type={self.msg_type}, Value: {self.value})"
