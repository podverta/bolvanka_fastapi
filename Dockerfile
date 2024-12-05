# Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN mkdir /app/screenshots
RUN chmod -R 777 /app/screenshots

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libgbm-dev \
    libpango1.0-0 \
    fonts-liberation \
    chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install pyppeteer
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium


COPY ./app /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE $FASTAPI_PORT

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${FASTAPI_PORT} --reload"]
