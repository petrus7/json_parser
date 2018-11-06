import os
import unittest
from json import JSONDecodeError

from json_parser.data_provider import DataProvider, FileDataSource, ServiceDataSource
from json_parser.json_checker import JsonChecker
from json_parser.param_validator import ParamValidator, NotAUrl, NotAFilePath, TooManyParams


class TestJSONChecker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.valid_json =  '''{"education":[{"education_org":"Universit\u00e0 Commerciale 'Luigi Bocconi'","degrees":["CLEACC - Degree in Economics and Management for Arts, Culture and Communication"],"end":"2006","start":"2000"},{"education_org":"WU (Vienna University of Economics and Business)","degrees":["Summer University"],"end":"2002","start":"2002"},{"education_org":"Liceo Ginnasio Statale S.M.Legnani","degrees":["Maturit\u00e0 Classica"],"end":"2000","start":"1995"}], "company":{"company_name":"Waters"}}'''
        cls.not_valid_json = '''{'a':1}'''

    def test_is_valid_json(self):
        json_checker = JsonChecker()
        self.assertIsNotNone(json_checker.create_user_dict(self.valid_json))
        self.assertRaises(JSONDecodeError, json_checker.create_user_dict, self.not_valid_json)
        pass

    def test_mach_company_constraint(self):
        company = 'Waters'
        json_checker = JsonChecker()
        user = json_checker.create_user_dict(self.valid_json)
        self.assertTrue(json_checker.user_fit_company(company, user))
        company = 'imaginary company'
        self.assertFalse(json_checker.user_fit_company(company, user))
        company = None
        self.assertTrue(json_checker.user_fit_company(company, user))

    def test_mach_education_constraint(self):
        education = 'Vienna University'
        json_checker = JsonChecker()
        user = json_checker.create_user_dict(self.valid_json)
        self.assertTrue(json_checker.user_fit_education(education, user))
        education = 'imaginary university'
        self.assertFalse(json_checker.user_fit_education(education, user))
        education = None
        self.assertTrue(json_checker.user_fit_education(education, user))




class TestParamValidator(unittest.TestCase):

    def test_check_params(self):

        try:
            with open('test.txt','w') as file:
                validator = ParamValidator({
                    'source': 'test.txt',
                    'education':'imaginary',
                    'company':'imaginary',
                    'http': False,
                    'file': True
                })
                self.assertTrue(validator.are_params_valid())
            os.remove('test.txt')
        except:
            print('Cannot create fake file')
        validator = ParamValidator({
            'source':'no_a_apath',
            'education':'imaginary',
            'company':'imaginary',
            'http': False,
            'file': True
        })
        self.assertRaises(NotAFilePath, validator.are_params_valid)
        validator = ParamValidator({
            'source': 'not_a_url',
            'education': 'imaginary',
            'company': 'imaginary',
            'http': True,
            'file': False
        })
        self.assertRaises(NotAUrl, validator.are_params_valid)

        validator = ParamValidator({
            'source': 'not_a_url',
            'education': 'imaginary',
            'company': 'imaginary',
            'http': True,
            'file': True
        })
        self.assertRaises(TooManyParams, validator.are_params_valid)


class TestDataProvider(unittest.TestCase):

    def test_apply_correct_data_provider(self):
        params = {
            'source': 'not_a_url',
            'education': 'imaginary',
            'company': 'imaginary',
            'http': True,
            'file': False
        }
        data_provider = DataProvider()
        data_source = data_provider.create_source(params)
        self.assertTrue(isinstance(data_source, ServiceDataSource))

        params = {
            'source': 'not_a_url',
            'education': 'imaginary',
            'company': 'imaginary',
            'http': False,
            'file': True
        }
        data_source = data_provider.create_source(params)
        self.assertTrue(isinstance(data_source, FileDataSource))



if __name__ == '__main__':
    unittest.main()
