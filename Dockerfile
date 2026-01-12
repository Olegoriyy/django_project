FROM python:3.12-slim    

ENV PYTHONUNBUFFERED=1  
ENV PYTHONDONTWRITEBYTECODE=1  
ENV POETRY_VERSION=2.2.1  

RUN groupadd -r groupdjango && useradd -r -g groupdjango userdjango
RUN pip install --upgrade pip
RUN pip install poetry "poetry==${POETRY_VERSION}"

# 3) НЕ создавать виртуальное окружение в контейнере
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock README.md ./

# 5) устанавливаем зависимости
# --no-interaction чтобы без вопросов
# --no-ansi чтобы логи были нормальные
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

USER userdjango
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]




