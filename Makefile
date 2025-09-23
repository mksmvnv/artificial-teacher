.PHONY: check fix
.PHONY: revision upgrade downgrade

SRC ?= src/

# Code quality (Ruff, Mypy)
check:
	uv run ruff check $(SRC)
	uv run mypy $(SRC)

fix:
	uv run ruff check --fix $(SRC)
	uv run ruff format $(SRC)


# Database (Alembic)

.PHONY: revision upgrade downgrade

revision:
	uv run alembic revision --autogenerate -m "$(msg)"

upgrade:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade "$(rev)"

