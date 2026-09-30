#!/bin/bash

# Environment to run
getawscreds --account 066-dev  # for dev/qa

ln -s ../src/data.csv .
PYTHONPATH=$PWD/../:$PWD/../src pytest -p no:warnings --cov=$PWD/../ --cov-report term-missing .
# PYTHONPATH=$PWD/.. pytest -p no:warnings --cov=src --cov-report term --cov-report html:coverage.html .
rm -f data.csv
