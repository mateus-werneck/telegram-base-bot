import os
from typing import Callable

from pytz import timezone
from telegram import ParseMode
from telegram.ext import (CommandHandler, Defaults, Dispatcher, Filters,
                          MessageHandler)
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.updater import Updater
from telegram.update import Update

from App.Lib.Bot.context import BotContext
from App.Lib.Bot.handler import BotHandler
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotClient(AbstractSingleton):
    def __init__(self):
        self.updater = None

        self.__set_client()
        self.__add_message_handler()

    def get_client(self) -> Updater:
        return self.updater

    def __set_client(self):
        tzinfo = timezone('America/Sao_Paulo')
        defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=tzinfo)
        token = os.environ.get('API_TOKEN')
        self.updater = Updater(token, use_context=True, defaults=defaults)

    def __add_message_handler(self):
        self.get_dispatcher()\
            .add_handler(MessageHandler(Filters.text, self.reply_message))

    def add_command_handler(self, command: str, callback_function:
                            Callable[[Update, CallbackContext], None]):
        self.get_dispatcher()\
            .add_handler(CommandHandler(command, callback_function))

    def get_dispatcher(self) -> Dispatcher:
        return self.get_client().dispatcher

    def reply_message(self, update: Update, context: CallbackContext):
        BotContext.instance().init(update, context)
        BotHandler.instance().check_user_has_permission()
        

