.PHONY: run migrate

init: 
	uv sync
	source .venv/bin/activate

run:
	python manage.py runserver


migrate:
	python manage.py migrate


migrations:
	python manage.py makemigrations
