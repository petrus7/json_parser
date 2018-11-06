from json_parser.param_validator import ParamValidator


class UsersDataFilter(object):

    EDUCATION_KEY = 'education'
    COMPANY_KEY = 'company'
    UNIVERSITY_NAME_KEY = 'education_org'
    COMPANY_NAME_KEY = 'company_name'

    def __init__(self, params: dict):
        self.params = params
        self.param_validator = ParamValidator(params)
        # self.data_source

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
        return [],[]
