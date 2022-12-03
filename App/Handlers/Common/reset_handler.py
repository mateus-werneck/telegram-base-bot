from App.Data.Helpers.message_helper import gear_icon
from App.Lib.Bot.chat import BotChat
from App.Lib.Bot.mode import BotMode
from App.Lib.Log.logger import Logger
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
        self.__clear_active_handlers()

    def __clear_active_handlers(self):    
        handlers = self.get_handlers()
        self.__save_active_handlers(handlers)
        
        for handler in handlers:
            if handler != 'ResetHandler':
                self.remove_handler(handler)
                
        self.__save_cleared_handlers(handlers)
    
    def __save_active_handlers(self, handlers: list):
        message = f'[*] Active handlers found: {handlers}'
        Logger.instance().info(message, context=self)

    def __save_cleared_handlers(self, handlers: list):
        cleared = str(len(handlers))
        message = f'[*] Cleared all {cleared} active handlers'
        Logger.instance().info(message, context=self)
