FROM python:3.14-rc-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

RUN poetry config virtualenvs.create false && poetry install --only main

EXPOSE 9617

CMD ["python", "-m", "pihole_exporter.main"]
