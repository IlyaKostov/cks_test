FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY ./api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./common /app/common
COPY ./api/app /app
COPY .env ./

CMD ["python", "app/"]
