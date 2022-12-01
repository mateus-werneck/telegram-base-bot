from App.Data.Helpers.message_helper import get_startup_message
from App.Lib.Bot.chat import BotChat
from App.Lib.Standard.abstract_handler_request import AbstractHandlerRequest


class StartHandler(AbstractHandlerRequest):

    def get_command(self) -> str:
        return 'start'

    def get_steps(self) -> list:
        return [self.start]

    def start(self):
        message = self.get_startup_message()
        BotChat.instance().send_text(message)
    
    def get_startup_message(self):
        return ''
