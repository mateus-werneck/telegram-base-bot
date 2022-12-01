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
        file_handler = logging.FileHandler(self.get_file_name(), encoding='utf-8')
        
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_file_name(self):
        return f"{os.environ['LOG_FOLDER']}/{os.environ['LOG_FILE']}"
    
    def debug(self, message: str, *additional_info):
        self.logger.debug(message)
        for debug in additional_info:
            self.logger.debug(debug)

    def info(self, message: str, *additional_info):
        self.logger.info(message)
        for info in additional_info:
            self.logger.info(info)

    def warning(self, message: str, *additional_info):
        self.logger.warning(message)
        for warning in additional_info:
            self.logger.warning(warning)

    def error(self, message: str, *additional_info):
        self.logger.error(message)
        for error in additional_info:
            self.logger.error(error)

    def critical(self, message: str, *additional_info):
        self.logger.critical(message)
        for critical in additional_info:
            self.logger.critical(critical)
