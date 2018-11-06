import os
import unittest
from json import JSONDecodeError
import io
import requests

from json_parser.data_filter import UsersDataFilter
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
            'source': 'https://jsonplaceholder.typicode.com/posts',
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


class TestFileDataSource(unittest.TestCase):

    def test_file_available(self):

        try:
            source = 'test.txt'
            with open(source,'w') as file:
                print('file created')
            users, malformed = FileDataSource(source).get_data()
            self.assertTrue(isinstance(users, list))
        except IOError:
            print('Cannot create fake file')
        finally:
            os.remove('test.txt')


class TestServiceDataSource(unittest.TestCase):

    def test_data_not_available(self):
        source = 'https://jsonpladddceholder.typicode.com/posts'
        provider = ServiceDataSource(source)
        self.assertRaises(requests.exceptions.ConnectionError, provider.get_data)

    def test_data_available(self):
        source = 'https://jsonplaceholder.typicode.com/posts'
        users, malformed = ServiceDataSource(source).get_data()
        self.assertTrue(isinstance(users, list))


class TestUserDataFilter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = '''{"education":[{"education_org":"Universit\u00e0 Commerciale 'Luigi Bocconi'","degrees":["CLEACC - Degree in Economics and Management for Arts, Culture and Communication"],"end":"2006","start":"2000"},{"education_org":"WU (Vienna University of Economics and Business)","degrees":["Summer University"],"end":"2002","start":"2002"},{"education_org":"Liceo Ginnasio Statale S.M.Legnani","degrees":["Maturit\u00e0 Classica"],"end":"2000","start":"1995"}], "company":{"company_name":"Waters"}}'''
        cls.test_file_path = 'test_users.json'
        try:
            with open('test_users.json', 'w') as t_file:
                t_file.writelines([
                    '''{"company":{"company_name":"imaginary company 1"},"education":[{"education_org":"imaginary university 1"}]}\n''',
                    '''{"company":{"company_name":"imaginary company 2"},"education":[{"education_org":"imaginary university 2"}]}\n''',
                    '''{"company":{"company_name":"imaginary company 3"},"education":[{"education_org":"imaginary university 3"}]}\n'''
                ])
        except IOError as e:
            print(f'TEST suite failed: {e}')

    @classmethod
    def tearDownClass(cls):
        try:
            if os.path.exists(cls.test_file_path):
                os.remove(cls.test_file_path)
        except Exception as e:
            print(f'TEST suite failed: {e}')


    def test_mach_company_constraint(self):
        company = 'Waters'
        params = params = {
            'source': 'test_users.json',
            'education': 'imaginary university 1',
            'company': None,
            'http': False,
            'file': True
        }
        user_filter = UsersDataFilter(params)
        json_checker = JsonChecker()
        user = json_checker.create_user_dict(self.test_user)
        self.assertTrue(user_filter.user_fit_company(company, user))
        company = 'imaginary company'
        self.assertFalse(user_filter.user_fit_company(company, user))
        company = None
        self.assertTrue(user_filter.user_fit_company(company, user))

    def test_mach_education_constraint(self):
        education = 'Vienna University'
        params = {
            'source': 'test_users.json',
            'education': 'imaginary university 1',
            'company': None,
            'http': False,
            'file': True
        }
        user_filter = UsersDataFilter(params)
        json_checker = JsonChecker()
        user = json_checker.create_user_dict(self.test_user)
        self.assertTrue(user_filter.user_fit_education(education, user))
        education = 'imaginary university'
        self.assertFalse(user_filter.user_fit_education(education, user))
        education = None
        self.assertTrue(user_filter.user_fit_education(education, user))

    def test_filter_users_by_education(self):

            params = params = {
                'source': 'test_users.json',
                'education': 'imaginary university 1',
                'company': None,
                'http': False,
                'file': True
            }
            user_filter = UsersDataFilter(params)
            users, not_valid = user_filter.filter()
            self.assertEqual(len(users), 1)

            params = params = {
                'source': 'test_users.json',
                'education': None,
                'company': 'imaginary company 1',
                'http': False,
                'file': True
            }
            user_filter = UsersDataFilter(params)
            users, not_valid = user_filter.filter()
            self.assertEqual(len(users), 1)

            params = params = {
                'source': 'test_users.json',
                'education': None,
                'company': None,
                'http': False,
                'file': True
            }
            user_filter = UsersDataFilter(params)
            users, not_valid = user_filter.filter()
            self.assertEqual(len(users), 3)


if __name__ == '__main__':
    unittest.main()
