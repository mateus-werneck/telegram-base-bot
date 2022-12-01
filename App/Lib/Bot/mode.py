from App.Lib.Log.logger import Logger
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotMode(AbstractSingleton):
    def __init__(self):
        self.mode = None

    def get_mode(self):
        return self.mode

    def set_mode(self, mode: object):
        self.mode = mode
        mode_name = mode.get_handler_name()
        Logger.instance().info(f'[{mode_name}] Started mode.')

    def clear_mode(self):
        self.mode = None
        
    def has_mode(self):
        return self.mode is not None
