from abc import ABC, abstractmethod
from traceback import format_exc

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from App.Lib.Bot.client import BotClient
from App.Lib.Bot.context import BotContext
from App.Lib.Bot.mode import BotMode
from App.Lib.Errors.user_not_allowed_exception import UserNotAllowedException
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
        self.__add_command_handler()

    def __add_command_handler(self):
        bot = BotClient.instance()
        command = self.get_command()
        bot.add_command_handler(command, self.execute)

    def __set_bot_mode(self):
        BotMode.instance().set_mode(self)

    def execute(self, update: Update = None, context: CallbackContext = None):
        try:
            BotContext.instance().init(update, context)
        except UserNotAllowedException:
            Logger.instance().warning('User not allowed to execute handler.')
            return

        self.__set_bot_mode()
        self.next()
        self.__handle_step()

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
            self.step()
            self.save_log()
            self.finish()
        except Exception:
            message = f'[*] Failed to execute step: "{self.step.__name__}".'
            Logger.instance().error(self.format_log(message), format_exc())
            self.finish(True)

    def finish(self, force: bool = False):
        if not self.should_finish(force):
            return
        BotMode.instance().clear_mode()
        self.__delete()

    def should_finish(self, force: bool):
        if force and not self.is_last_step():
            return True
        return self.is_last_step()

    def is_last_step(self):
        last_step = self.get_steps().pop()
        return last_step.__name__ == self.step.__name__

    def __delete(self):
        class_name = self.get_handler_name()
        del self.__instances[class_name]

    def save_log(self):
        message = f'[*] Excecuted step: "{self.step.__name__}".'
        Logger.instance().info(self.format_log(message))

    def format_log(self, message: str):
        class_name = self.get_handler_name()
        return message.replace('*', class_name)

    def get_handler_name(self):
        return self.__class__.__name__
