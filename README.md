# PhotoGram

[![CircleCI](https://circleci.com/gh/toransahu/photogram.svg?style=shield)](https://circleci.com/gh/toransahu/photogram)
[![codecov](https://codecov.io/gh/toransahu/photogram/branch/master/graph/badge.svg)](https://codecov.io/gh/toransahu/photogram)
[![CodeStyle](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/) 


A photo collection/sharing hub.

# Prerequisites
- Python >= 3.7, pip
- MySQL Server, Client (optional)

# Installation
- Install dependencies
```bash
pip install pipenv
cd photogram
pipenv install
```

- Migrate
```bash
pipenv shell
cd src
python manage.py migrate
```

# Run
- Start application server
```
python manage.py runserver
```

will run the server at `127.0.0.1:8000` by default.

# API Documentation
- open following link to explore the API docs  
[`http://127.0.0.1:8000`](http://127.0.0.1:8000)

# Code Coverage
```bash
coverage run --source='.' manage.py test
coverage report -m
```
