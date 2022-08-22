import os
import sys
import json

def test_coverage(test_file='test.py', limit=80):
    os.system(f'coverage run {test_file}')
    os.system('coverage json')
    test_coverage = open('coverage.json')
    test_coverage = json.load(test_coverage)

    print(f"Asserting Test Coverage (with minimum limit of {limit}):")
    if(test_coverage['totals']['percent_covered'] < limit):
        print(f"ERROR: Total test coverage is {test_coverage['totals']['percent_covered']}% which is less than {limit}%")
        sys.exit(1)
    else:
        print(f"Total: {test_coverage['totals']['percent_covered']}%")


    for file in test_coverage['files'].keys():
        if(file != test_file):
            file_coverage = test_coverage['files'][file]['summary']['percent_covered']
            if(file_coverage < limit):
                print(f"ERROR: {file} has a test coverage of {file_coverage}% which is less than {limit}%")
                sys.exit(1)
            else:
                print(f"{file}: {file_coverage}%")

if __name__ == '__main__':
    test_coverage(test_file='test.py', limit=80)
