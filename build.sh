#!/usr/bin/env bash

# this is for renderer build for staging stuffs
set -o errexit

uv sync --frozen

uv run python manage.py collectstatic --noinput
uv run python manage.py migrate
uv run python manage.py seed
