from json_parser.data_provider import DataProvider
from json_parser.param_validator import ParamValidator


class UsersDataFilter(object):

    EDUCATION_KEY = 'education'
    COMPANY_KEY = 'company'
    UNIVERSITY_NAME_KEY = 'education_org'
    COMPANY_NAME_KEY = 'company_name'

    def __init__(self, params: dict):
        self.params = params
        self.param_validator = ParamValidator(params)
        self.data_source = DataProvider().create_source(params)

    def user_fit_education(self, education:str, user:dict):
        if not education:
            return True

        for education_data in user.get(self.EDUCATION_KEY, []):
            if education.lower().strip() in education_data.get(self.UNIVERSITY_NAME_KEY, '').lower().strip():
                return True

        return False

    def user_fit_company(self, company:str, user:dict):
        if not company:
            return True

        company_data = user.get(self.COMPANY_KEY, {})
        if len(company_data) == 0:
            company_name = ''
        else:
            company_name = company_data.get(self.COMPANY_NAME_KEY, '')
        if company.lower().strip() in company_name.lower().strip():
            return True
        return False

    def filter(self):
        filtered_users = []
        if self.param_validator.are_params_valid():
            users, malformed = self.data_source.get_data()
            for user in users:
                if self.user_fit_company(self.params.get('company'), user) and self.user_fit_education(self.params.get('education'), user):
                    filtered_users.append(user)
            return filtered_users, malformed
        return [], []
