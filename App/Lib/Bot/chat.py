
from App.Lib.Bot.context import BotContext
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotChat(AbstractSingleton):

    def __init__(self):
        super().__init__()
        self.bot_context = BotContext.instance()

    def send_text(self, message: str):
        chat_id = self.bot_context.get_chat_id()
        self.get_bot().send_message(chat_id, message)

    def send_callback_query(self, reply_markup: dict, text: str = ''):
        chat_id = self.bot_context.get_chat_id()
        self.get_bot().send_message(chat_id, text, reply_markup)

    def delete_message(self):
        message_id = self.bot_context.get_message_id()
        chat_id = self.bot_context.get_chat_id()
        try:
            self.get_bot().delete_message(chat_id, message_id)
        except Exception:
            return
        
    def get_bot(self):
        self.bot_context.get_context().bot
