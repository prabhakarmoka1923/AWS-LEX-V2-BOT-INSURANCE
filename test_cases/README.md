## Prerequisites:
Libraries to install: pytest and pytest_cov
### Commands to setup library:
```
pip install pytest
pip install pytest_cov
```
## Controlling test cases:
1. Main controller function for running assertions is run_assertions.
2. It can be run for executing coverage or unit_test by defining the kwarg "test_type" which accepts "coverage" or "unit_test".
3. If you are running for "unit_test", we can controll the execution of it by kwarg "execute_for" which accepts
"all", "context", "message_chips".
4. all - will run complete json response, message, suggestion chips and context assertions.
5. context - will run only context assertions.
6. message_chip - will run message and suggestion chips assertions.

## Steps to create the test cases:
1. Add request json payload to payloads/request folder
2. For the response json payload, add response json to payloads/response folder
3. Go to test_lex.py, create a new function inside class
4. Every function should start with "test"
5. Coverage html will be created showing complete code coverage
6. For Testing via CMD, execute the bash:

## For Testing via CMD:
1) Enable proxy environment to get aws role
```
setproxy
````
2) Get aws role list and select your role
```
getawscreds
```
3) Execute run-test.sh file to run test_lex.py
```
./run-test.sh
```