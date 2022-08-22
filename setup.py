precommit = '''#!/bin/sh
Make test || exit 1'''

with open('.git/hooks/pre-commit', 'w') as f:
    f.write(precommit)

makefile = '''test:
	python test.py
	python test_coverage.py'''

with open('Makefile', 'w') as f:
    f.write(makefile)