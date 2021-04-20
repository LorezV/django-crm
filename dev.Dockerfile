FROM python:3.9-slim-buster

WORKDIR /opt/services/crm-django-and-bot/src/

ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.5 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.local/bin" \
  # django
  DJANGO_SETTINGS_MODULE=crm.settings.local

# Upgrade & Update system
RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y

# Install poetry
RUN apt-get install curl -y \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# Copy only requirements to cache them in docker layer
COPY ./pyproject.toml ./poetry.lock ./

# Project initialization
RUN poetry install

# Creating folders, and files for a project
COPY ./ ./
