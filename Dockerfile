# Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY ./app /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE $FASTAPI_PORT

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${FASTAPI_PORT} --reload"]
