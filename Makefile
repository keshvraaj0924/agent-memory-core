.PHONY: install dev test lint format-check typecheck check run docker-up docker-down migrate benchmark

install:
	python -m pip install -e ".[dev]"

dev:
	uvicorn main:app --reload

test:
	pytest

lint:
	ruff check .

format-check:
	ruff format --check .

typecheck:
	mypy app

check: lint format-check typecheck test

run:
	uvicorn main:app --host 0.0.0.0 --port 8000

docker-up:
	docker compose up --build

docker-down:
	docker compose down

migrate:
	alembic upgrade head

benchmark:
	python scripts/benchmark_retrieval.py
