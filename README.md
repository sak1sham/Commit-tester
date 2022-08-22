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

2. Run setup.py file to create prerequisite files.
    ```bash
    python setup.py
    ```
   Following files will be created:
    1. Makefile
    2. test_commit.py

3. ```test.py``` file is essential to test the code. A template has been added to the ```test.py``` file. After making changes, when you try to commit the code, the following changes are tested:
    1. Test cases should be successfull

    2. Test coverage should not be less than the set limit (default=80%), for both: individual files and the entire repo
    
    3. Lint Score should be atleast the set limit (default=75.0/100.0) for all modified files