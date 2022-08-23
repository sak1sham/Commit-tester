import argparse

parser = argparse.ArgumentParser(description="script to setup and secure commits")
parser.add_argument("--testfile", help="The path of your test file (default: test.py)", default="test.py", type=str, required=False)
parser.add_argument("--coverage", help="The minimum testing coverage (default: 80)", default=80, type=int, required=False)
parser.add_argument("--lint", help="The minimum lint score out of 100 to pass (default: 75.0)", default=75.0, type=float, required=False)
args, leftovers = parser.parse_known_args()


################################################################################
############### WRITE COMMIT TESTING FILE ######################################

test_coverage = '''import os
import sys
import json
import argparse
from git import Repo
import subprocess

class bcolors:
    HEADER = '\\033[95m'
    OKBLUE = '\\033[94m'
    OKCYAN = '\\033[96m'
    OKGREEN = '\\033[92m'
    WARNING = '\\033[93m'
    FAIL = '\\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\\033[1m'
    UNDERLINE = '\\033[4m'

def f_test_coverage(test_file='test.py', limit=80):
    try:
        result = subprocess.check_output(f'coverage run {test_file}', stderr=subprocess.STDOUT).decode('UTF-8')
    except subprocess.CalledProcessError as e:
        result = e.output.decode('UTF-8')
        print(f"{bcolors.FAIL}{result}{bcolors.ENDC}")
        sys.exit(1)
    os.system(f'coverage json --omit="{test_file}","test_commit.py","setup.py"')
    test_coverage = open('coverage.json')
    test_coverage = json.load(test_coverage)
    
    print(f"Asserting Test Coverage (with minimum limit of {limit}%):")
    if(test_coverage['totals']['percent_covered'] < limit):
        print(f"{bcolors.FAIL}ERROR: Total test coverage is {test_coverage['totals']['percent_covered']}% which is less than {limit}%{bcolors.ENDC}")
        sys.exit(1)
    else:
        print(f"{bcolors.OKGREEN}OK Total: {test_coverage['totals']['percent_covered']}%{bcolors.ENDC}")

    for file in test_coverage['files'].keys():
        if(file not in [test_file, 'test_commit.py', 'setup.py']):
            file_coverage = test_coverage['files'][file]['summary']['percent_covered']
            if(file_coverage < limit):
                print(f"{bcolors.FAIL}ERROR: {file} has a test coverage of {file_coverage}% which is less than {limit}%{bcolors.ENDC}")
                sys.exit(1)
            else:
                print(f"{bcolors.OKGREEN}OK {file}: {file_coverage}%{bcolors.ENDC}")


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
    ret_str = result
    substr = 'Your code has been rated at '
    pos_start = result.find(substr) + len(substr)
    result = result[pos_start:]
    pos_end = result.find('/')
    score = float(result[:pos_end])
    result = result[pos_end+1:]
    pos_complete = result.find(' ')
    max_score = float(result[:pos_complete])
    lint_score = score*100/max_score
    return ret_str, lint_score


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to test the test coverage for your changes and for the entire repo")
    parser.add_argument("--file", help="The path of your test file (default: test.py)", default="test.py", type=str, required=False)
    parser.add_argument("--limit", help="The minimum testing coverage (default: 80)", default=80, type=int, required=False)
    parser.add_argument("--lint", help="The minimum lint score out of 100 to pass (default: 75.0)", default=75.0, type=float, required=False)
    args, leftovers = parser.parse_known_args()
    
    print(f"\\n\\n{bcolors.HEADER}{bcolors.UNDERLINE}{bcolors.BOLD}TESTING SCRIPTS AND TEST-COVERAGE{bcolors.ENDC}")
    f_test_coverage(test_file=args.file, limit=args.limit)
    
    print(f"\\n\\n{bcolors.HEADER}{bcolors.UNDERLINE}{bcolors.BOLD}TESTING LINT SCORE (OUT OF 100.0){bcolors.ENDC}")
    list_changed_files = get_changed_files()
    for filepath in list_changed_files:
        if(filepath in ['requirements.txt', 'setup.py', 'README.md', '.gitignore']):
            continue
        lint_result, score = checkLint(filepath)
        if(score < args.lint):
            print(f"{bcolors.FAIL}ERROR: Lint Score for {filepath} is {score} (less than {args.lint}, not sufficient):{bcolors.ENDC}")
            print(lint_result)
            sys.exit(1)
        else:
            print(f"{bcolors.OKGREEN}{filepath}: {score}{bcolors.ENDC}")
    
    print(f"\\n\\n{bcolors.HEADER}{bcolors.UNDERLINE}{bcolors.BOLD}TESTING SUCCESSFUL{bcolors.ENDC}\\n\\n")
'''

with open('test_commit.py', 'w', encoding='utf-8') as f:
    f.write(test_coverage)



############################################################################
################### WRITE MAKEFILE #########################################

makefile = f'''test:
	python test_commit.py --file={args.testfile} --limit={args.coverage} --lint={args.lint}'''

with open('Makefile', 'w') as f:
    f.write(makefile)



############################################################################
################# WRITE PRE-COMMIT FILE ####################################

precommit = '''#!/bin/sh
Make test || exit 1'''

with open('.git/hooks/pre-commit', 'w') as f:
    f.write(precommit)

