#! /bin/bash
rm -rf .coverage
coverage run --source=. --branch --omit=*test*.py -m nose2 -v &&
coverage report --fail-under=100 &&
echo "Success"
