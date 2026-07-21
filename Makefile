.PHONY: run init migrate superuser shell dbshell test lint

init:
		uv sync 

activate:
		source .venv/Scripts/activate
		source .venv/lib/activate

run:
		python manage.py runserver

migrate:
		python manage.py makemigrations
		python manage.py migrate
		python manage.py showmigrations

superuser:
		python manage.py create_admin

shell:
		python manage.py shell

dbshell:
		python manage.py dbshell

test:
		python manage.py test

lint:
		djlint . --reformat


