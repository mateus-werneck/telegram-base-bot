class BotMode():
    def __init__(self):
        self.mode = None

    def get_mode(self):
        return self.mode

    def set_mode(self, mode: object):
        self.mode = mode

    def clear_mode(self):
        self.mode = None
        
    def has_mode(self):
        return self.mode is not None

