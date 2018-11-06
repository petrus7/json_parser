import json


class WrongFormatException(json.JSONDecodeError):
    pass


class JsonChecker(object):

    EDUCATION_KEY = 'education'
    COMPANY_KEY = 'company'
    UNIVERSITY_NAME_KEY = 'education_org'
    COMPANY_NAME_KEY = 'company_name'

    def create_user_dict(self, json_line:str):
        j_data = json.loads(json_line)
        if self.EDUCATION_KEY not in j_data:
            raise WrongFormatException(f'Bad formated data: lack of {self.EDUCATION_KEY}')
        if self.EDUCATION_KEY not in j_data:
            raise WrongFormatException(f'Bad formated data: lack of {self.COMPANY_KEY}')
        return j_data

    def check_dict_format(self, user_data:dict):
        if self.EDUCATION_KEY not in user_data:
            raise WrongFormatException(f'Bad formated data: lack of {self.EDUCATION_KEY}')
        if self.EDUCATION_KEY not in user_data:
            raise WrongFormatException(f'Bad formated data: lack of {self.COMPANY_KEY}')

