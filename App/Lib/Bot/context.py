
import os

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from App.Lib.Errors.user_not_allowed_exception import UserNotAllowedException
from App.Lib.Log.logger import Logger
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotContext(AbstractSingleton):

    def __init__(self):
        self.update = None
        self.context = None

    def init(self, update: Update = None, context: CallbackContext = None):
        if update is not None:
            self.set_update(update)
        if context is not None:
            self.set_context(context)
        if update is not None and context is not None:
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
        chat_id = self.get_chat_id()
        Logger.instance().info(f'[BotContext] Authenticating User {str(chat_id)}')

        if str(chat_id) in allowed:
            return

        exception = UserNotAllowedException(chat_id)
        update = self.get_update()
        Logger.instance().warning(exception.message, update)
        raise exception
    
    def get_bot(self):
        context = self.get_context()
        return context.bot
    
    def get_chat_id(self):
        context = self.get_context()
        chat_id, data = context._chat_id_and_data
        return chat_id

    def get_message_id(self):
        update = self.get_update()
        message = getattr(update, 'message')

        if hasattr(update, 'callback_query'):
            message = update.callback_query.message

        return getattr(message, 'message_id', 0)
