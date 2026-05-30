FROM python:3.14-rc-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev \
    && poetry config virtualenvs.create false && poetry install --only main \
    && apt-get purge -y gcc python3-dev && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

EXPOSE 9617

CMD ["pihole-exporter"]
