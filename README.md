# PhotoGram

[![CircleCI](https://circleci.com/gh/toransahu/photogram.svg?style=shield)](https://circleci.com/gh/toransahu/photogram)
[![codecov](https://codecov.io/gh/toransahu/photogram/branch/master/graph/badge.svg)](https://codecov.io/gh/toransahu/photogram)
[![CodeStyle](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/) 


A photo collection/sharing hub.
- Built using Python and Django (DRF) with test driven development (TDD) approach
- Contains APIs for:
	- USERS : Register new user, login, logout etc.
	- ROLES : View role, registered user role,  admin/staff role etc.
	- SHARING : Share photos using shareable link via token auths & link expiration feature
	- CRUDing : Create, retrieve, update, and destroy photos

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

If using MySQL then create databse (optional)
```SQL
create database photogram CHARACTER SET utf8;
```

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
