# Commit-tester

Use this boilerplate code inside your repo to test it before committing or pushing changes.
1. Install "Make"
    ```bash
    # For windows (https://chocolatey.org/install)
    choco install make

    # For mac (https://brew.sh/)
    brew install make

    # For linux (https://linux.die.net/man/8/apt-get)
    apt-get -y install make
    ```

2. Run setup.py file to create pre-commit hooks to test your code before committing
    ```bash
    python setup.py
    ```

3. ```test.py``` file is required to test the code. A template has been added to the ```test.py``` file. After making changes, when you try to commit the code, the following changes are tested:
    a) Test cases should be successfull
    b) Test coverage should not be less than 80% (for individual files, as well as entire repo)