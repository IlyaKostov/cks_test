FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY ./monitoring/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./common /app/common
COPY ./monitoring/monitoring_app /app
COPY .env ./

CMD ["python", "app/main.py"]
