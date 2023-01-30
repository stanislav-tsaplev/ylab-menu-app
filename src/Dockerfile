FROM python:3.10-slim
WORKDIR /src
ENV PYTHONPATH=/app

COPY requirements.txt alembic.ini ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY .docker-app.env ./.env
COPY migrations/ ./migrations
COPY app/ ./app
