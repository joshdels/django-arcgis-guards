.PHONY: run migrate

run:
	python manage.py runserver


migrate:
	python manage.py migrate


migrations:
	python manage.py makemigrations
