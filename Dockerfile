FROM python:3.11-slim-buster
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev
COPY . /app/
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]

