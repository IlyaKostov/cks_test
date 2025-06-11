FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY ./bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./bot/bot_app /app
COPY .env ./

CMD ["python", "app/main.py"]
