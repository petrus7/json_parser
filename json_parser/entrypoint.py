import argparse

from json_parser.j_parser import filter_users


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file_path', help='File to parse path', required=True, type=str)
    parser.add_argument(
        '--company', help='Filter users from company', required=False, type=str)
    parser.add_argument(
        '--education', help='Filter users from university', required=False, type=str)
    args = parser.parse_args()
    f_path = args.file_path
    company_const = args.company
    education_const = args.education
    try:
        users, not_valid_data = filter_users(f_path, company_const, education_const)
        print('Following users fit given requirements:')
        for user in users:
            print(user)
        if not_valid_data:
            print('Following users are not in valid format:')
            for user in not_valid_data:
                print(user)
    except FileNotFoundError as e:
        print(f'CANNOT FIND FILE: {f_path} CHECK PATH PARAMETER')
    except IOError as e:
        print(f'CANNOT OPEN FILE: {f_path} TRY AGAIN.')
    except:
        print('Something goes wrong conntact technical support')
