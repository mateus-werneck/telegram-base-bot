from abc import ABC, abstractmethod
from traceback import format_exc

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from App.Lib.Bot.chat import BotChat
from App.Lib.Bot.client import BotClient
from App.Lib.Bot.context import BotContext
from App.Lib.Bot.mode import BotMode
from App.Lib.Errors.Auth.user_not_allowed_exception import \
    UserNotAllowedException
from App.Lib.Log.logger import Logger


class AbstractHandlerRequest(ABC):
    __instances = {}

    @classmethod
    def instance(cls):
        class_name = cls.__name__
        if not cls.__instances.get(class_name):
            cls.__instances[class_name] = cls()
        return cls.__instances[class_name]

    @abstractmethod
    def get_command(self) -> str:
        pass

    @abstractmethod
    def get_steps(self) -> list:
        pass

    def __init__(self):
        self.step = None
        self.bot_context = BotContext.instance()
        self.__add_command_handler()

    def __add_command_handler(self):
        bot = BotClient.instance()
        command = self.get_command()
        if command == '':
            return
        bot.add_command_handler(command, self.execute)

    def get_handler_name(self):
        return self.__class__.__name__

    def get_handlers(self):
        return list(self.__instances)

    def reset_handler(self, handler: str):
        if not self.has_handler(handler):
            return
        self.__instances[handler].step = None
        message = f'[*] Reseting handler: {handler}'
        Logger.instance().info(message, context=self)

    def has_handler(self, handler:str):
        return handler in self.get_handlers()
    
    def execute(self, update: Update = None, context: CallbackContext = None):
        if not self.__handle_update(update, context):
            return

        if not self.__should_execute_next_step():
            return self.finish(True)

        self.__set_bot_mode()
        self.next()
        self.__handle_step()

    def __handle_update(self, update: Update = None,
                        context: CallbackContext = None):
        try:
            self.bot_context.init(update, context)
            return True
        except UserNotAllowedException:
            message = '[*] User not allowed to execute handler.'
            Logger.instance().warning(message, context=self)
            return False

    def __should_execute_next_step(self) -> bool:
        if self.bot_context.has_go_back_button():
            return self.go_back()
        elif self.bot_context.has_exit_button():
            BotChat.instance().extract_callback_data()
            return False

        return True

    def go_back(self) -> bool:
        message = f'[*] Going back from step: {self.step.__name__}'
        Logger.instance().info(message, context=self)

        if self.is_first_step():
            BotChat.instance().extract_callback_data()
            return False

        steps = self.get_steps()
        self.step = steps[self.get_current_step() - 1]
        BotChat.instance().extract_callback_data()
        return True

    def is_first_step(self):
        return self.get_current_step() == 0

    def __set_bot_mode(self):
        BotMode.instance().set_mode(self)

    def next(self):
        steps = self.get_steps()
        next_step = self.get_current_step() + 1
        self.step = steps[next_step]

    def get_current_step(self):
        if self.step is None:
            return -1
        steps = self.get_steps()
        return steps.index(self.step)

    def __handle_step(self):
        try:
            step_result = self.step()
            self.__save_step_log()
            force_finish = self.__should_force_finish(step_result)
            self.finish(force_finish)
        except Exception:
            message = f'[*] Failed to execute step: "{self.step.__name__}".'
            Logger.instance().error(message, format_exc(), context=self)
            self.finish(True)
    
    def __should_force_finish(self, step_result):
        return not (step_result is None or step_result)
    
    def __save_step_log(self):
        message = f'[*] Excecuted step: "{self.step.__name__}".'
        Logger.instance().info(message, context=self)

    def finish(self, force: bool = False):
        if not self.should_finish(force):
            return

        BotMode.instance().clear_mode()
        handler = self.get_handler_name()
        self.reset_handler(handler)

    def should_finish(self, force: bool):
        if force:
            return True
        return self.is_last_step()

    def is_last_step(self):
        last_step = self.get_steps().pop()
        return last_step.__name__ == self.step.__name__

    def is_mode(self, mode: str):
        answer = BotContext.instance().get_callback_data()
        return answer == mode
    
    def get_logger(self):
        return Logger.instance()
    
    def send_message(self, message: str):
        BotChat.instance().send_text(message)
        
    def delete_message(self):
        BotChat.instance().delete_message()
    
    def get_text_data(self):
        return BotContext.instance().get_text_data()
    
    def has_valid_text_data(self):
        data = self.get_text_data()
        return data is not None and data != '' and data
    
    def get_callback_data(self):
        return BotChat.instance().extract_callback_data()
    

