
## Indy Python wrapper functional test

This is a Python wrapper functional test for Indy. The tests are not driven by any unit test framework but are standalone python scripts.

This Python wrapper functional test currently requires python 3.6, base58.

### How to run

After building successfully the Indy SDK for Python, you need to run the commands below so that could run the tests:

- Install base58 dependency with pip install: 
```
     python3.6 -m pip install base58.
```
- Setup PYTHONPATH: 
```
    export PYTHONPATH=$PYTHONPATH:your_repo_location/functional_tests 
```


#### Then run:
- Run one test case:
```
    python3.6 your_repo_location/functional_tests/test_scripts/wallet/open_wallet.py
```
- Run a folder test case:
```
    python3.6 your_repo_location/functional_tests/test_runner.py -d your_test_folder
```

- Run all test cases in the project:
```
    python3.6 your_repo_location/functional_tests/test_runner.py -rd
```

#### Generate the htlm report:
- Get the summary report for all the run
```
    python3.6 your_repo_location/functional_tests/reporter.py
```

