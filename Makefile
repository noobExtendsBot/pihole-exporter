.PHONY: check fix

check:
	poetry run black --check src/ tests/
	poetry run isort --check src/ tests/
	poetry run mypy src/

fix:
	poetry run black src/ tests/
	poetry run isort src/ tests/
