
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from App.Lib.Bot.mode import BotMode
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotContext(AbstractSingleton, BotMode):

    def __init__(self):
        super().__init__()
        self.update = None
        self.context = None

    def init(self, update: Update, context: CallbackContext):
        self.set_update(update)
        self.set_context(context)

    def get_update(self) -> Update:
        return self.update

    def set_update(self, update: Update):
        self.update = update

    def get_context(self) -> CallbackContext:
        return self.context

    def set_context(self, context: CallbackContext):
        self.context = context
