import os
import sys
import json

test_file = 'test.py'

os.system(f'coverage run {test_file}')
os.system('coverage json')
test_coverage = open('coverage.json')

test_coverage = json.load(test_coverage)

for file in test_coverage['files'].keys():
    if(file != test_file):
        file_coverage = test_coverage['files'][file]['summary']['percent_covered']
        if(file_coverage < 80):
            print(f"ERROR: {file} has a test coverage of {file_coverage} which is less than 80%")
            sys.exit(1)