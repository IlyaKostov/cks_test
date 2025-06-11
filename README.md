# 🛒 Price Monitoring Microservices

Микросервисное приложение для мониторинга цен на товары с разных сайтов, на данный момент только Мвидео.

## 📦 Состав проекта

- **api_service** — HTTP API для добавления, просмотра и удаления товаров.
- **monitor_service** — Сервис для проверки цен по URL-адресам.
- **bot_service** — Сервис для взаимодействия пользователя с API.
- **RabbitMQ** — брокер сообщений для обработки задач мониторинга.
- **PostgreSQL** — основная база данных.
- **Docker Compose** — инструмент для запуска всех компонентов вместе.

## 🚀 Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/IlyaKostov/cks_test.git
cd cks_test
```

### 2. Создать файл .env

MVID_CITY_ID=CityCZ_975;  
MVID_REGION_ID=1;  
MVID_TIMEZONE_OFFSET=3;  
MVID_REGION_SHOP=S002;  


DB_HOST=db  
DB_PORT=5432  
DB_USER=postgres  
DB_PASS=postgres  
DB_NAME=  

MODE=DEV

API_HOST=localhost  
API_PORT=8000

RABBITMQ_HOST=rabbitmq

TG_BOT_TOKEN=

### 3. Запуск с помощью Docker Compose
```bash
docker-compose up --build
```
Откройте браузер и перейдите по адресу: http://localhost:8000/docs — интерактивная документация API (Swagger UI).

| Метод  | URL                                     | Описание                              |
|--------|-----------------------------------------|---------------------------------------|
| POST   | `/products/add_product`                 | Добавить новый продукт                |
| GET    | `/products/products_list`               | Получить список всех продуктов        |
| DELETE | `/products/delete_product/{product_id}` | Удалить продукт по ID                 |
| GET    | `/prices/{product_id}`                  | Получить историю цен на продукт по ID |



## ⚙️ Архитектура взаимодействия

1. Пользователь взаимодействует с тг-ботом для отправки команд на сервер.
2. `bot-service` Получает запрос пользователя и направляет на сервер.
3. `api_service` сохраняет, либо удаляет продукт в базу и отправляет задачу на мониторинг через Dramatiq, 
либо получая любой другой запрос, обращается к БД и предоставляет данные.
4. `monitor_service` получает задачу, делает запрос по product_id, получает текущую цену и сверяет 
с ценой которая была ранее, при наличии изменений добавляет новую цену в историю.

<br><p align=center><img alt="img" height="600" src="/architecture.png" width="1000"/></p>


## 🛠️ Технологии

* **FastAPI** — для API
* **SQLAlchemy + asyncpg** — для работы с БД
* **Dramatiq** — для фоновых задач
* **APScheduler** — для периодичных задач
* **RabbitMQ** — брокер сообщений
* **Alembic** — миграции
* **Aiogram** — тг-бот
* **Docker / Docker Compose** — для контейнеризации

[//]: # (## ✅ TODO &#40;развитие проекта&#41;)

[//]: # ()
[//]: # (* [ ] Хранение истории цен)

[//]: # (* [ ] Уведомления при изменении цены)

[//]: # (* [ ] Веб-интерфейс)

[//]: # (* [ ] Авторизация и личный кабинет)
