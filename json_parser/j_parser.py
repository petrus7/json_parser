import json

COMPANY_KEY = 'company'
COMPANY_NAME_KEY = 'company_name'
EDUCATION_KEY = 'education'
UNIVERSITY_NAME_KEY = 'education_org'


def filter_users(file_path: str, company: str, education: str):
    filtered_users = []
    not_valid_data = []
    with open(file_path, 'r') as json_data:
        for line in json_data:
            user = create_user_from_json_str(line)
            if user:
                try:
                    if user_fit_company(company, user) and user_fit_education(education, user):
                        filtered_users.append(user)
                except:
                    not_valid_data.append(user)
            else:
                not_valid_data.append(line)

    return filtered_users, not_valid_data


def user_fit_company(company: str, user: dict):
    if not company:
        return True

    company_data = user.get(COMPANY_KEY, {})
    if len(company_data) == 0:
        company_name = ''
    else:
        company_name = company_data.get(COMPANY_NAME_KEY, '')
    if company.lower().strip() in company_name.lower().strip():
        return True
    return False


def user_fit_education(education: str, user: dict):
    if not education:
        return True

    for education_data in user.get(EDUCATION_KEY, []):
        if education.lower().strip() in education_data.get(UNIVERSITY_NAME_KEY, '').lower().strip():
            return True

    return False


def create_user_from_json_str(json_str: str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None

