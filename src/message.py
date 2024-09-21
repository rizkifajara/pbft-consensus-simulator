class Message:
    def __init__(self, sender, msg_type: any, content: any):
        self.sender = sender
        self.type = msg_type
        self.content = content