import abc

class DataSource(abc.ABC):

    def __init__(self, data_source):
        self._data_source = data_source

    @abc.abstractmethod
    def get_data(self):
        pass


class FileDataSource(DataSource):

    def get_data(self):
        with open(self._data_source, 'r') as file:
            return file.readlines()


class ServiceDataSource(DataSource):

    def get_data(self):
        pass


class DataProvider(object):

    def create_source(self, params):
        if params.get('file'):
            return FileDataSource(params.get('source'))
        return ServiceDataSource(params.get('source'))
