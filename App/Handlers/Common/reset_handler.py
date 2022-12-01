from App.Data.Helpers.message_helper import gear_icon
from App.Lib.Bot.chat import BotChat
from App.Lib.Bot.mode import BotMode
from App.Lib.Standard.abstract_handler_request import AbstractHandlerRequest


class ResetHandler(AbstractHandlerRequest):

    def get_command(self) -> str:
        return 'cancel'

    def get_steps(self) -> list:
        return [self.reset]

    def reset(self):
        message = f'{gear_icon()} Bot reconfigurado.'
        BotChat.instance().send_text(message)
        BotMode.instance().clear_mode()
        self.clear_all()
