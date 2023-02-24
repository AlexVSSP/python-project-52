install:
		poetry install

uninstall:
		python3 -m pip uninstall hexlet-code

test:
		poetry run python manage.py test

test-coverage:
		poetry run coverage run manage.py test
		poetry run coverage xml
		poetry run coverage report

req:
		poetry export --without-hashes --format=requirements.txt > requirements.txt

start:
		poetry run python manage.py runserver

gunicorn:
		poetry run gunicorn task_manager.wsgi

lint:
		poetry run flake8 task_manager
