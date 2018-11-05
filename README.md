# PhotoGram

A photo collection/sharing hub.

# Prerequisites
- Python >= 3.6, Pip
- MySQL Server, Client

# Installation
- install dependencies
```bash
pip install pipenv
cd `photogram`
pipenv install
```

- Migrate
```bash
pipenv shell
cd src
python manage.py migrate
python manage.py runserver
```

# Code Coverage
```bash
coverage run --source='.' manage.py test
coverage report -m
```
