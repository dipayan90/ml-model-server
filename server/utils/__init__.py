import logging
import traceback
from json import load
import os.path


class AppLogger:

    def __init__(self, log_level=None):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M')
        if log_level == "info":
            logging.getLogger('').setLevel(logging.INFO)
        elif log_level == "warn":
            logging.getLogger('').setLevel(logging.WARN)
        elif log_level == 'error':
            logging.getLogger('').setLevel(logging.ERROR)

    def get_logger(self):
        return logging.getLogger('')


class BaseError(Exception):

    code = None
    default_message = "API Error: "
    error_metric = None

    def __init__(self, message=default_message):
        self.message = message

    def response(self):
        """http response"""
        return {'message': self.message, "trace": traceback.format_exc()}, self.code


class NotFoundError(BaseError):
    code = 404


class RequestError(BaseError):
    code = 400


class ServerError(BaseError):
    code = 500


class Config:

    def __init__(self, config_file_path: str = "config.json"):
        self.__app_config = None
        self.config_file_path = config_file_path

    @property
    def app_config(self) -> dict:
        if self.__app_config:
            return self.__app_config
        else:
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path) as json_file:
                    self.__app_config = load(json_file)
                return self.__app_config
            raise ServerError(f"Config file couldn't be found at location: {self.config_file_path}")
