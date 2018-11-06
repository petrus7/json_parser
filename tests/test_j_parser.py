import unittest
from json import JSONDecodeError

from tests.json_checker import JsonChecker


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
        self.assertTrue(json_checker.user_fit_company(company, user))
        company = None
        self.assertTrue(json_checker.user_fit_company(company, user))

    def test_mach_education_constraint(self):
        education = 'Vienna University'
        json_checker = JsonChecker()
        user = json_checker.create_user_dict(self.valid_json)
        self.assertTrue(json_checker.user_fit_education(education, user))
        education = 'imaginary university'
        self.assertTrue(json_checker.user_fit_education(education, user))
        education = None
        self.assertTrue(json_checker.user_fit_education(education, user))



if __name__ == '__main__':
    unittest.main()
