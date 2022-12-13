import os

from pytz import timezone
from telegram import ParseMode
from telegram.ext import (CallbackQueryHandler, CommandHandler, Defaults,
                          Dispatcher, Filters, MessageHandler)
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.updater import Updater
from telegram.update import Update

from App.Lib.Bot.chat import BotChat
from App.Lib.Bot.context import BotContext
from App.Lib.Bot.mode import BotMode
from App.Lib.Errors.Auth.user_not_allowed_exception import \
    UserNotAllowedException
from App.Lib.Log.logger import Logger
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotClient(AbstractSingleton):
    def __init__(self):
        self.updater = None
        self.__set_client()

    def get_client(self) -> Updater:
        return self.updater
    
    def get_dispatcher(self) -> Dispatcher:
        return self.get_client().dispatcher

    def __set_client(self):
        tzinfo = timezone('America/Sao_Paulo')
        defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=tzinfo)
        token = os.environ.get('API_TOKEN')
        self.updater = Updater(token, use_context=True, defaults=defaults)

    def add_message_handler(self):
        message_handler = MessageHandler(Filters.text, self.reply_message)
        self.get_dispatcher().add_handler(message_handler)

    def add_command_handler(self, command: str, callback_function):
        command_handler = CommandHandler(command, callback_function)
        self.get_dispatcher().add_handler(command_handler)

        message = f'[*] Added CommandHandler for {command}:'\
                                  + f'"{callback_function.__name__}"'
        Logger.instance().info(message, context=self)

    def add_callback_handler(self, menu: dict, callback_function):
        for line in menu['inline_keyboard']:
            for button in line:
                self.__add_button_handler(button, callback_function)

    def __add_button_handler(self, button: dict, callback_function):
        callback_handler = CallbackQueryHandler(
            callback_function, pattern=button['callback_data'])

        self.get_dispatcher().add_handler(callback_handler)

        message = f"Added CallbackHandler for \
                    {button['callback_data']}: {callback_function.__name__}"
        Logger.instance().info(message, context=self)

    def reply_message(self, update: Update, context: CallbackContext):
        try:
            BotContext.instance().init(update, context)
        except UserNotAllowedException:
            return

        if BotMode.instance().has_mode():
            mode = BotMode.instance().get_mode()
            mode.instance().execute()
            return

        message = 'Para continuar escolha uma função.\n'\
            + '\nSe estiver em duvida digite /ajuda'
        BotChat.instance().send_text(message)
