.PHONY: check fix

check:
	poetry run black --check src/ tests/
	poetry run isort --check src/ tests/
	poetry run mypy src/
	poetry run python -m unittest discover -s tests/

fix:
	poetry run black src/ tests/
	poetry run isort src/ tests/
