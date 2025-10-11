.PHONY: run check fix revision upgrade downgrade current history

SRC ?= src

# Application

all: fix check run

run:
	uv run python -m $(SRC).main

# Code quality

check:
	uv run ruff check $(SRC)
	uv run mypy $(SRC)

fix:
	uv run ruff format $(SRC)
	uv run ruff check --fix $(SRC)

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

