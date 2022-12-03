
from App.Lib.Bot.context import BotContext
from App.Lib.Log.logger import Logger
from App.Lib.Standard.abstract_singleton import AbstractSingleton


class BotChat(AbstractSingleton):

    def __init__(self):
        super().__init__()
        self.bot_context = BotContext.instance()

    def get_bot_context(self):
        return self.bot_context
    
    def send_text(self, message: str):
        telegram_bot = self.get_bot_context().get_bot()
        chat_id = self.get_bot_context().get_chat_id()
        telegram_bot.send_message(chat_id, message)

    def send_callback_query(self, title: str, reply_markup: dict):
        telegram_bot = self.get_bot_context().get_bot()
        chat_id = self.get_bot_context().get_chat_id()
        telegram_bot.send_message(chat_id, text=title, reply_markup=reply_markup)

    def delete_message(self):
        telegram_bot = self.get_bot_context().get_bot()
        message_id = self.get_bot_context().get_message_id()
        chat_id = self.get_bot_context().get_chat_id()
        
        try:
            telegram_bot.delete_message(chat_id, message_id)
        except Exception as e:
            message = f'[*] Failed to delete message: {str(message_id)}'
            Logger.instance().critical(message, e, context=self)
            return

    def extract_callback_data(self):
        bot_context = self.get_bot_context()
        
        if not bot_context.has_callback_data():
            return
        
        self.delete_message()
        data = bot_context.get_callback_data()
        message = f'[*] Extracting Callback Data: {str(data)}'
        Logger.instance().info(message, context=self)
        return data
        