.PHONY: install update format lint test run

install:
	poetry install

update:
	poetry update

format:
	poetry run ruff format .

lint:
	poetry run ruff check .
	poetry run mypy .

test:
	poetry run pytest

run:
	poetry run uvicorn main:app --reload

all: install format lint test
