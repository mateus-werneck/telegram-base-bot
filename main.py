from App.Lib.Bot.client import BotClient

if __name__ == '__main__':
    BotClient.instance()\
        .get_client()\
        .start_polling()
