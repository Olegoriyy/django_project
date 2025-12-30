FROM python:3.13-slim

WORKDIR /app




RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*


COPY pyproject.toml poetry.lock* ./

RUN pip install poetry
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False




