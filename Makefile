.PHONY: run init migrate superuser shell dbshell test lint

init:
		uv sync 

run:
		python manage.py runserver

migrate:
		python manage.py makemigrations
		python manage.py migrate

superuser:
		python manage.py createsuperuser --username admin --email admin@email.com

shell:
		python manage.py shell

dbshell:
		python manage.py dbshell

test:
		python manage.py test

lint:
		djlint . --reformat


