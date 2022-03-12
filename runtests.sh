#! /bin/bash
rm -rf .coverage
coverage run --source=. --branch --omit=*test*.py -m nose2 -v &&
coverage report --show-missing --fail-under=60 &&
echo "Success"
