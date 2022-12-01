
from App.Lib.Bot.context import BotContext
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotChat(AbstractSingleton):

    def __init__(self):
        super().__init__()
        self.bot_context = BotContext.instance()

    def get_bot_context(self):
        return self.bot_context
    
    def send_text(self, message: str):
        context = self.get_bot_context().get_context()
        chat_id = self.get_bot_context().get_chat_id()
        context.bot.send_message(chat_id, message)

    def send_callback_query(self, reply_markup: dict, text: str = ''):
        context = self.get_bot_context().get_context()
        chat_id = self.get_bot_context().get_chat_id()
        context.bot.send_message(chat_id, text, reply_markup)

    def delete_message(self):
        context = self.get_bot_context().get_context()
        message_id = self.get_bot_context().get_message_id()
        chat_id = self.get_bot_context().get_chat_id()
        try:
            context.bot.delete_message(chat_id, message_id)
        except Exception:
            return
