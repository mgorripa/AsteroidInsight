# Virtual environment settings
VENV_NAME := .venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate
PYTHON := $(VENV_NAME)/bin/python3

# Django settings
DJANGO_SETTINGS_MODULE := astrostellar.settings

# Commands
INSTALL_REQUIREMENTS := pip install -r requirements.txt
RUN_SERVER := $(PYTHON) manage.py runserver 8000
MIGRATE := $(PYTHON) manage.py migrate
MAKE_STATIC := $(PYTHON) manage.py collectstatic

# Targets
.PHONY: venv install run migrate static

venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_NAME)

install:
	@echo "Installing requirements..."
	@. $(VENV_ACTIVATE); \
	$(INSTALL_REQUIREMENTS)

run:
	@echo "Starting Django development server..."
	@. $(VENV_ACTIVATE); \
	$(RUN_SERVER)

migrate:
	@echo "Applying migrations..."
	@. $(VENV_ACTIVATE); \
	$(MIGRATE)

static:
	@echo "Collecting statics..."
	@. $(VENV_ACTIVATE); \
	$(MAKE_STATIC)

help:
	@echo "make commands"
	@echo "make venv : creates a new .venv folder with environment"
	@echo "make install : installs requirements.txt packages in .venv"
	@echo "make run : run django project"
	@echo "make migrate : gets all migrations for django project"
	@echo "make static : collects all static files"