import os
import urllib.parse


class NotAUrl(Exception):
    pass


class TooManyParams(Exception):
    pass


class NotAFilePath(Exception):
    pass


class ParamValidator(object):

    def __init__(self, params: dict):
        self.__params = params

    def are_params_valid(self):
        if self.__params.get('file') and self.__params.get('http'):
            raise TooManyParams('Specify file or web type not both')
        elif self.__params.get('file') and not os.path.exists(self.__params.get('source')):
            raise NotAFilePath('Given file does not exist')
        elif self.__params.get('http'):
            result = urllib.parse.urlparse(self.__params.get('source'))
            if not all([result.scheme,result.netloc,result.path]):
                raise NotAUrl('Not a valid url')
        return True


