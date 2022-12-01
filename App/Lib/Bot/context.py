
import os

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from App.Lib.Bot.chat import BotChat
from App.Lib.Errors.user_not_allowed_exception import UserNotAllowedException
from App.Lib.Log.logger import Logger
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotContext(AbstractSingleton):

    def __init__(self):
        self.update = None
        self.context = None

    def init(self, update: Update = None, context: CallbackContext = None):
        if update is None and context is None:
            return
        self.set_update(update)
        self.set_context(context)
        self.check_user_has_permission()

    def get_update(self) -> Update:
        return self.update

    def set_update(self, update: Update):
        self.update = update

    def get_context(self) -> CallbackContext:
        return self.context

    def set_context(self, context: CallbackContext):
        self.context = context
    
    def check_user_has_permission(self):
        allowed = os.environ['ALLOWED_USERS'].split(',')
        chat_id = BotChat.instance().get_chat_id()

        if str(chat_id) in allowed:
            return

        exception = UserNotAllowedException(chat_id)
        update = BotContext.instance().get_update()
        Logger.instance().warning(exception.message, update)
        raise exception
