from App.Lib.Bot.client import BotClient
from App.Lib.Log.logger import Logger


def start_client():
    BotClient.instance()\
        .get_client()\
        .start_polling()
    Logger.instance().info('[BotClient] Bot started successfully.')

if __name__ == '__main__':
    start_client()
