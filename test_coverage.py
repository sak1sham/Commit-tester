import os
import sys
import json
import argparse

def test_coverage(test_file='test.py', limit=80):
    os.system(f'coverage run {test_file}')
    os.system('coverage json')
    test_coverage = open('coverage.json')
    test_coverage = json.load(test_coverage)

    print(f"Asserting Test Coverage (with minimum limit of {limit}%):")
    if(test_coverage['totals']['percent_covered'] < limit):
        print(f"ERROR: Total test coverage is {test_coverage['totals']['percent_covered']}% which is less than {limit}%")
        sys.exit(1)
    else:
        print(f"OK Total: {test_coverage['totals']['percent_covered']}%")


    for file in test_coverage['files'].keys():
        if(file not in [test_file, 'test_coverage.py']):
            file_coverage = test_coverage['files'][file]['summary']['percent_covered']
            if(file_coverage < limit):
                print(f"ERROR: {file} has a test coverage of {file_coverage}% which is less than {limit}%")
                sys.exit(1)
            else:
                print(f"OK {file}: {file_coverage}%")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="script to test the test coverage for your changes and for the entire repo")
    parser.add_argument("--file", help="The path of your test file (default: test.py)", type=str, required=False)
    parser.add_argument("--limit", help="The minimum testing coverage (default: 80)", type=int, required=False)
    args, leftovers = parser.parse_known_args()

    if(args.file is None):
        args.file = "test.py"
    if(args.limit is None):
        args.limit = 80
    test_coverage(test_file=args.file, limit=args.limit)
