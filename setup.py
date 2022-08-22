import os

precommit = '''#!/bin/sh
Make test || exit 1'''

with open('.git/hooks/pre-commit', 'w') as f:
    f.write(precommit)