import json
from abc import ABC, abstractmethod

from requests import Request, Response, Session
from requests.compat import urljoin

from App.Lib.Errors.Client.invalid_request_exception import \
    InvalidRequestException
from App.Lib.Log.logger import Logger


class ExternalConn(ABC):
    __instances = dict()

    @classmethod
    def instance(cls):
        class_name = cls.__name__
        if cls.__instances.get(class_name) is None:
            cls.__instances[class_name] = cls()
        return cls.__instances[class_name]

    def __init__(self):
        self.client = None
        self.headers = dict()
        self.request = None
        
        self.set_client()

    @abstractmethod
    def get_base_url(self) -> str:
        return ''

    def set_client(self):
        self.client = Session()

    def get_client(self):
        return self.client

    def get_request(self) -> Request:
        if not isinstance(self.request, Request):
            raise InvalidRequestException(api=self.__class__.__name__)
        return self.request

    def set_request(self, method: str, path: str, json=None, params=None):
        url = self.get_request_path(path)
        self.request = Request(method, url, json=json, params=params)

    def get_request_path(self, route: str):
        return urljoin(self.get_base_url(), route)

    def get(self, route: str, query_params=None):
        self.set_request('GET', route, None, query_params)
        return self.__send()

    def post(self, route: str, body = None):
        self.set_request('POST', route, body)
        return self.__send()

    def patch(self, route: str, body=None, query_params=None):
        self.set_request('PATCH', route, body, query_params)
        return self.__send()

    def delete(self, route: str, query_params=None):
        self.set_request('DELETE', route, None, query_params)
        return self.__send()

    def __send(self):
        current_request = self.get_request()
        self.__save_request_log(current_request)

        try:
            response = self.get_client().send(current_request.prepare())
            self.__save_response_log(response)
        except Exception as e:
            response = self.__treat_error_to_response(e)
            self.__save_error_log(response)
            return response

        return self.__treat_response_data(response)

    def __save_log(self, message: str):
        Logger.instance().info(message, context=self)

    def __save_request_log(self, request: Request):
        message = f'{request.method.upper()} Sending request to {request.url}'
        self.__save_log(message)

    def __save_response_log(self, response: Response):
        message = f'{response.status_code} Received response from {response.url}'
        self.__save_log(message)
        
        data = self.__treat_response_data(response)
        message = f'Data Received {json.dumps(data)}'
        self.__save_log(message)

    def __save_error_log(self, response: dict):
        message = f'Error on request {json.dumps(response)}'
        self.__save_log(message)

    def __treat_response_data(self, response: Response):
        try:
            return response.json()
        except ValueError:
            return {}

    def __treat_error_to_response(self, exception: object):
        response = {}
        if hasattr(exception, 'code'):
            response['code'] = exception.code
        if hasattr(exception, 'reason'):
            response['reason'] = exception.reason
        return response
