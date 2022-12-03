import logging
import os

from App.Lib.Standard.abstract_singleton import AbstractSingleton


class Logger(AbstractSingleton):
    def __init__(self):
        self.logger = logging.Logger('BotLogger')
        self.initiate_logger()

    def initiate_logger(self):
        self.set_file_handler()
        self.logger.setLevel(logging.INFO)

    def set_file_handler(self):
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(
            self.get_file_name(), encoding='utf-8')

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_file_name(self):
        return f"{os.environ['LOG_FOLDER']}/{os.environ['LOG_FILE']}"

    def debug(self, message: str, *args, **kwargs):
        self.__handle_logging(message, self.logger.debug, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        self.__handle_logging(message, self.logger.info, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self.__handle_logging(message, self.logger.warning, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self.__handle_logging(message, self.logger.error, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        self.__handle_logging(message, self.logger.critical, *args, **kwargs)

    def __handle_logging(self, message: str, callback, *args, **kwargs):
        message = self.__format_log(message, kwargs)
        callback(message)
        [callback(additional) for additional in args]

    def format_log(self, message: str, formatting: dict):
        if formatting.get('context'):
            context_name = formatting.get('context').__class__.__name__
            message = message.replace('*', context_name)
        return message

