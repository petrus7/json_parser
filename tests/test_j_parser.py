import os
import unittest

from json_parser.j_parser import user_fit_education, create_user_from_json_str, user_fit_company, filter_users


class TestJSONParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = '''{"id":28218624,"linkedin_id":"alessandramontrasio","linkedin_profile_url":"https:\/\/www.linkedin.com\/in\/alessandramontrasio","last_name":"Montrasio","first_name":"Alessandra","num_connections":500,"num_jobs":10,"location":{"country_name":"France","city_name":"Paris"},"industry":"Food & Beverages","job_title":"Nestl\u00c3\u00a9 Pure Life Global Communication Lead","company":{"company_name":"Waters"},"job_history":[{"job_title":"Nestl\u00e9 Pure Life Digital Lead - Global Business Unit","company_name":"Nestl\u00e9 Waters","company_intern_id":"nestl-waters","start":"October 2015"},{"job_title":"Digital Brand Development and Communication Manager Buitoni","company_name":"Nestle","company_intern_id":"nestle-s-a-","end":"September 2015","start":"January 2013"},{"job_title":"Digital Acceleration Team - permanent member","company_name":"Nestl\u00e9","company_intern_id":"nestle-s-a-","end":"September 2015","start":"January 2013"},{"job_title":"Brand Manager Buitoni","company_name":"Nestl\u00e9","company_intern_id":"nestle-s-a-","end":"December 2012","start":"April 2011"},{"job_title":"Product Manager Beverage","company_name":"Nestl\u00e9","company_intern_id":"nestle-s-a-","end":"April 2011","start":"March 2010"},{"job_title":"Product Manager Frozen Food","company_name":"Nestl\u00e9","company_intern_id":"nestle-s-a-","end":"March 2010","start":"October 2008"},{"job_title":"Junior Product Manager","company_name":"Bel","company_intern_id":"bel","end":"September 2008","start":"September 2007"},{"job_title":"Assistant Brand Manager","company_name":"Bel","company_intern_id":"bel","end":"September 2007","start":"September 2006"},{"job_title":"intern","company_name":"Deutsches Museum","end":"September 2003","start":"February 2003"}],"job_history_extended":{"2018\/2":{"company_name":"Global Business Unit","job_title":"Nestl\u00e9 Pure Life Digital Lead"},"2018\/7":{"job_title":"Nestl\u00c3\u00a9 Pure Life Global Communication Lead"},"2018\/5":{"job_title":"Nestl\u00e9 Pure Life Global Digital Lead"}},"skills":["Brand Architecture","Brand Management","Brand management","Consumer Products","Customer Insight","Digital Marketing","FMCG","International Marketing","Market Analysis","Marketing Communications","Marketing Strategy","Marketing communication","Product Development","Product Innovation","Product Management","Segmentation","Strategy"],"also_viewed":["guendalina-armitano-94073b11","valeria-aguzzi-ba516ba","gloria-iannuzzi-b8a30528","andreaantoniogalli","philippearmand","federica-lupoli-659a1516","anna-maestrelli-64b75b1","barbara-vita-43525b","beatrice-milani-6183a04","elisabettacorazza"],"languages":["Italian","English","French","German","Spanish"],"season":"2018-09-01","education":[{"education_org":"Universit\u00e0 Commerciale 'Luigi Bocconi'","degrees":["CLEACC - Degree in Economics and Management for Arts, Culture and Communication"],"end":"2006","start":"2000"},{"education_org":"WU (Vienna University of Economics and Business)","degrees":["Summer University"],"end":"2002","start":"2002"},{"education_org":"Liceo Ginnasio Statale S.M.Legnani","degrees":["Maturit\u00e0 Classica"],"end":"2000","start":"1995"}]}'''
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
