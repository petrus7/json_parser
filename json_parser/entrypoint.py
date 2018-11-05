import argparse

from json_parser.j_parser import filter_users


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', help='File to parse path', required=True, type=str)
    parser.add_argument('--company', help='Filter users from company', required=False, type=str)
    parser.add_argument('--education', help='Filter users from university', required=False, type=str)
    args = parser.parse_args()
    print(args.file_path)
    print(args.company)
    print(args.education)
    filter_users()

