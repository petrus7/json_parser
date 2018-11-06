from json_parser.param_validator import ParamValidator


class UsersDataFilter(object):
    def __init__(self, params: dict):
        self.params = params
        self.param_validator = ParamValidator(params)
        # self.data_source




    def filter(self):
        return [],[]
