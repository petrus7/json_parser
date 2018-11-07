import argparse

from json_parser.data_filter import UsersDataFilter
from json_parser.param_validator import NotAUrl, NotAFilePath


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source', help='File to parse path', required=True, type=str)
    parser.add_argument(
        '--company', help='Filter users from company', required=False, type=str)
    parser.add_argument(
        '--education', help='Filter users from university', required=False, type=str)
    parser.add_argument('--web', dest='file', action='store_false', required=False)
    parser.set_defaults(file=True)
    args = parser.parse_args()
    params = {
        'source': args.source,
        'education': args.education,
        'company': args.company,
        'file': args.file
    }

    try:
        users, not_valid_data = UsersDataFilter(params).filter()
        print('Following users fit given requirements:')
        for user in users:
            print(user)
        if not_valid_data:
            print('Following users are not in valid format:')
            for user in not_valid_data:
                print(user)
    except NotAFilePath as e:
        print(f'CANNOT OPEN FILE: {e} TRY AGAIN.')
    except NotAUrl as e:
        print(f'Cannot fetch data: {e}')
    except:
        print("somethiong goes wrong contact technical support")


if __name__ =='__main__':
    main()