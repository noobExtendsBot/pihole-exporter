FROM python:3.14-rc-slim

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libffi-dev \
    && pip install poetry \
    && poetry config virtualenvs.create false && poetry install --only main \
    && apt-get purge -y build-essential && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

EXPOSE 9617

CMD ["pihole-exporter"]
