.PHONY: check fix

SRC ?= src/


check:
	uv run ruff check $(SRC)
	uv run mypy $(SRC)

fix:
	uv run ruff check --fix $(SRC)
	uv run ruff format $(SRC)
