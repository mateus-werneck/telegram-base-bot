
import os

from App.Lib.Bot.chat import BotChat
from App.Lib.Bot.context import BotContext
from App.Lib.Errors.user_not_allowed_exception import UserNotAllowedException
from App.Lib.Log.logger import Logger
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotHandler(AbstractSingleton):

    def __init__(self):
        self.handler = None

    def check_user_has_permission(self):
        allowed = os.environ['ALLOWED_USERS'].split(',')
        chat_id = BotChat.instance().get_chat_id()

        if str(chat_id) in allowed:
            return

        exception = UserNotAllowedException(chat_id)
        update = BotContext.instance().get_update()
        Logger.instance().warning(exception.message, update)
        raise exception
