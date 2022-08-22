import argparse

parser = argparse.ArgumentParser(description="script to setup and secure commits")
parser.add_argument("--testfile", help="The path of your test file (default: test.py)", type=str, required=False)
parser.add_argument("--coverage", help="The minimum testing coverage (default: 80)", type=int, required=False)
args, leftovers = parser.parse_known_args()

if(args.testfile is None):
    args.testfile = "test.py"
if(args.coverage is None):
    args.coverage = 80

############################################################################
################# WRITE PRE-COMMIT FILE ####################################

precommit = '''#!/bin/sh
Make test || exit 1'''

with open('.git/hooks/pre-commit', 'w') as f:
    f.write(precommit)

############################################################################
################### WRITE MAKEFILE #########################################

makefile = f'''test:
	python test_commit.py --file={args.testfile} --limit={args.coverage}'''

with open('Makefile', 'w') as f:
    f.write(makefile)

################################################################################
###############   WRITE TEST COVERAGE FILE #####################################

test_coverage = '''import os
import sys
import json
import argparse
from git import Repo
import subprocess

def f_test_coverage(test_file='test.py', limit=80):
    os.system(f'coverage run {test_file}')
    os.system(f'coverage json --omit="{test_file}","test_commit.py","setup.py"')
    test_coverage = open('coverage.json')
    test_coverage = json.load(test_coverage)
    
    print(f"Asserting Test Coverage (with minimum limit of {limit}%):")
    if(test_coverage['totals']['percent_covered'] < limit):
        print(f"ERROR: Total test coverage is {test_coverage['totals']['percent_covered']}% which is less than {limit}%")
        sys.exit(1)
    else:
        print(f"OK Total: {test_coverage['totals']['percent_covered']}%")

    for file in test_coverage['files'].keys():
        if(file not in [test_file, 'test_commit.py', 'setup.py']):
            file_coverage = test_coverage['files'][file]['summary']['percent_covered']
            if(file_coverage < limit):
                print(f"ERROR: {file} has a test coverage of {file_coverage}% which is less than {limit}%")
                sys.exit(1)
            else:
                print(f"OK {file}: {file_coverage}%")


def get_changed_files():
    repo = Repo('./')
    o = repo.remotes.origin
    o.pull()[0]
    list_check = repo.untracked_files
    for item in repo.index.diff(None):
        list_check.append(item.a_path)
    return list_check


def checkLint(filepath):
    try:
        result = subprocess.check_output(f'pylint {filepath}', stderr=subprocess.STDOUT).decode('UTF-8')
    except subprocess.CalledProcessError as e:
        result = e.output.decode('UTF-8')
    substr = 'Your code has been rated at '
    pos_start = result.find(substr) + len(substr)
    result = result[pos_start:]
    pos_end = result.find('/')
    score = float(result[:pos_end])
    result = result[pos_end+1:]
    pos_complete = result.find(' ')
    max_score = float(result[:pos_complete])
    lint_score = score*100/max_score
    return lint_score


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="script to test the test coverage for your changes and for the entire repo")
    parser.add_argument("--file", help="The path of your test file (default: test.py)", type=str, required=False)
    parser.add_argument("--limit", help="The minimum testing coverage (default: 80)", type=int, required=False)
    parser.add_argument("--lint", help="The minimum lint score out of 100 to pass (default: 75)", type=int, required=False)
    args, leftovers = parser.parse_known_args()

    if(args.file is None):
        args.file = "test.py"
    if(args.limit is None):
        args.limit = 80
    if(args.lint is None):
        args.lint = 75
    
    print("\\n\\n--------- TESTING SCRIPTS AND TEST-COVERAGE ----------")
    f_test_coverage(test_file=args.file, limit=args.limit)
    
    print("\\n\\n---------------- TESTING LINT SCORE ------------------")
    list_changed_files = get_changed_files()
    for filepath in list_changed_files:
        if(filepath in ['requirements.txt', 'setup.py', 'README.md', '.gitignore']):
            continue
        score = checkLint(filepath)
        if(score < args.lint):
            print(f"ERROR: Lint Score for {filepath} is {score} (less than prescribed score of  {args.lint})")
            sys.exit(1)
        else:
            print(f"Lint Score for {filepath} is {score}")
    print("\\n\\n----------------- TESTING SUCCESSFUL ------------------\\n\\n")
'''

with open('test_commit.py', 'w', encoding='utf-8') as f:
    f.write(test_coverage)