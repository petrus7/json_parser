import abc
from json import JSONDecodeError

from json_parser.json_checker import JsonChecker


class DataSource(abc.ABC):

    def __init__(self, data_source):
        self._data_source = data_source

    @abc.abstractmethod
    def get_data(self):
        pass


class FileDataSource(DataSource):

    def get_data(self):
        ret = []
        malformed = []
        json_checker = JsonChecker()
        with open(self._data_source, 'r') as file:
            for line in file:
                try:
                    ret.append(json_checker.create_user_dict(line))
                except JSONDecodeError as e:
                    malformed.append(line)
        return ret, malformed


class ServiceDataSource(DataSource):

    def get_data(self):
        pass


class DataProvider(object):

    def create_source(self, params):
        if params.get('file'):
            return FileDataSource(params.get('source'))
        return ServiceDataSource(params.get('source'))
