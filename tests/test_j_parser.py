import os
import unittest

from json_parser.j_parser import user_fit_education, create_user_from_json_str, user_fit_company, filter_users


class TestJSONParser(unittest.TestCase):

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



    def test_create_user_from_json_str(self):
        user = create_user_from_json_str(self.test_user)
        self.assertIsNotNone(user)
        user = create_user_from_json_str('''{'ala':'makota'}''')
        self.assertIsNone(user)

    def test_user_fit_company(self):
        company = 'Waters'
        user = create_user_from_json_str(self.test_user)
        self.assertTrue(user_fit_company(company, user))

    def test_user_not_fit_company(self):
        company = 'imaginary company'
        user = create_user_from_json_str(self.test_user)
        self.assertFalse(user_fit_company(company, user))

    def test_user_no_company_param(self):
        user = create_user_from_json_str(self.test_user)
        self.assertTrue(user_fit_company(None, user))

    def test_user_fit_education(self):
        education = 'Vienna University'
        user = create_user_from_json_str(self.test_user)
        self.assertTrue(user_fit_education(education, user))

    def test_user_not_fit_education(self):
        education = 'imaginary university'
        user = create_user_from_json_str(self.test_user)
        self.assertFalse(user_fit_education(education, user))

    def test_user_no_education_param(self):
        user = create_user_from_json_str(self.test_user)
        self.assertTrue(user_fit_education(None, user))

    def test_filter_users_file_not_exist(self):
        self.assertRaises(FileNotFoundError, filter_users, 'test_file', 'imaginary company', 'imaginary university')

    def test_filter_users_no_params(self):
        users, not_valid = filter_users(self.test_file_path, None, None)
        self.assertEqual(len(users), 3)

    def test_filter_users_company(self):
        users, not_valid = filter_users(self.test_file_path, 'imaginary company 1', None)
        self.assertEqual(len(users), 1)

    def test_filter_users_education(self):
        users, not_valid = filter_users(self.test_file_path, None, 'imaginary university 3')
        self.assertEqual(len(users), 1)


if __name__ == '__main__':
    unittest.main()
