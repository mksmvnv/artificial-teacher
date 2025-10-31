.PHONY: run check fix test revision upgrade downgrade current history

SRC ?= src
TESTS ?= tests

# Application

all: fix check run

run:
	uv run python -m $(SRC).main

# Code quality

check:
	uv run ruff check $(SRC) $(TESTS)
	uv run mypy $(SRC) $(TESTS)

fix:
	uv run ruff format $(SRC) $(TESTS)
	uv run ruff check --fix $(SRC) $(TESTS)

# Tests

test:
	uv run python -m pytest $(TESTS)/ -v

test-cov:
	uv run python -m pytest $(TESTS)/ --cov=src --cov-report=term-missing

test-cov-html:
	uv run python -m pytest $(TESTS)/ --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report: file://$(PWD)/htmlcov/index.html"

test-cov-fail:
	uv run python -m pytest $(TESTS)/ --cov=src --cov-fail-under=80

# Migrations

revision:
	uv run alembic revision --autogenerate -m "$(MSG)"

upgrade:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade "$(REV)"

current:
	uv run alembic current

history:
	uv run alembic history

