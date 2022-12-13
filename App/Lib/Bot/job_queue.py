from telegram.ext.callbackcontext import CallbackContext

from App.Lib.Bot.client import BotClient
from App.Lib.Client.marina_api import MarinaAPI
from App.Lib.Log.logger import Logger
from App.Lib.Standard.abstract_singleton import AbstractSingleton
from App.Lib.Treat.time_treat import treat_string_hour_to_time


class BotJobQueue(AbstractSingleton):

    def get_queue(self):
        bot_client = BotClient().instance().get_client()
        return bot_client.job_queue

    def __save_log(self, job: dict):
        deadline = job.get('when') if job.get('when') else job.get('time')
        message = f'Registering Job [{job.get("name")}] at {deadline}.'
        Logger.instance().info(message, context=self)

    def register_once(self, **kwargs):
        self.__save_log(kwargs)
        self.get_queue().run_once(**kwargs)
        return self

    def register_daily(self, **kwargs):
        self.__save_log(kwargs)
        self.get_queue().run_daily(**kwargs)
        return self
