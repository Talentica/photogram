# PhotoGram

A photo collection/sharing hub.

# Prerequisites
- Python >= 3.6, Pip
- MySQL Server, Client (optional)

# Installation
- Install dependencies
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
```

# Run
- Start application server
```
python manage.py runserver
```

will run server at `127.0.0.1:8000` by default.

# API Documentation
- open following link to explore the API docs
`http://127.0.0.1:8000`

# Code Coverage
```bash
coverage run --source='.' manage.py test
coverage report -m
```
