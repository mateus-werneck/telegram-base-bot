import os

from App.Lib.Bot.client import BotClient
from App.Lib.Log.logger import Logger
from init import Init


def start_client():
    bot = BotClient.instance()
    
    Init()
    
    bot.add_message_handler()
    bot.get_client().start_polling()
    Logger.instance().info('[BotClient] Bot started successfully.')

if __name__ == '__main__':
    start_client()
