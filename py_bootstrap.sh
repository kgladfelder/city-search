#!/bin/sh

export FLASK_APP=./city-search-api/index.py

#Windows sourcing.
source $(py -m pipenv --venv)/Scripts/activate
#Linux sourcing.
#source $(py -m pipenv --venv)/bin/activate

flask run -h 0.0.0.0