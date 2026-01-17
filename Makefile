.PHONY: all lint format format-check typecheck test test-cov check fix clean complexity docstyle docs docs-build

all: check

lint:
	uv run ruff check .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

typecheck:
	uv run ty check

test:
	uv run pytest

test-cov:
	uv run pytest --cov-report=html

check: lint format-check typecheck test

fix:
	uv run ruff check --fix .
	uv run ruff format .

complexity:
	@output=$$(uv run radon cc src/porkbun_mcp -n D -s); \
	if [ -n "$$output" ]; then \
		echo "$$output"; \
		echo "ERROR: Functions with complexity D or higher found"; \
		exit 1; \
	else \
		echo "Complexity check passed (no D+ functions)"; \
	fi

docstyle:
	uv run ruff check --select=D src/

docs:
	uv run mkdocs serve

docs-build:
	uv run mkdocs build

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov coverage.xml site
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
