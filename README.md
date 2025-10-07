# Applications Service

Тестовое задание для mediann.dev

---

## 1. Первичный запуск

1. Клонируйте репозиторий:

```bash
git clone <https://github.com/MrEclipse/mediann.dev.git>
cd test_for_mediann.dev
```

2. Создайте виртуальное окружение и активируйте его:

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate   # Linux/Mac
```

```cmd
.\.venv\Scripts\activate  # Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Запустите docker compose:

```bash
docker compose up --build
```

Приложение будет доступно на `http://localhost:8000`.
Сваггер по стандартному `http://localhost:8000/docs`.
---

## 2. Тест кейсы (Swagger)

**POST /applications**

* Ввод: JSON с `user_name` и `description`.
* ```
  {"user_name": "mark",
  "description": "big deal man"}
* Действие: Создать новое приложение.
* Ожидаемый результат: JSON с созданным приложением.
* ```
  {"id": 10,
  "user_name": "mark",
  "description": "big deal man",
  "created_at": "2025-10-06T23:11:15.027915Z"}
* Лог: `Сообщение отправлено в Kafka`.

**GET /applications**

* Ввод: Параметры `page` 4 и `size` 4.
* Действие: Получить список приложений.
* Ожидаемый результат: JSON-массив приложений.
* ```
  [{
    "id": 5,
    "user_name": "kakakaf6",
    "description": "string",
    "created_at": "2025-10-06T22:54:20.237931Z"
  },
  {
    "id": 4,
    "user_name": "kakakaf6",
    "description": "string",
    "created_at": "2025-10-06T22:54:20.068893Z"
  },
  {
    "id": 3,
    "user_name": "kakakaf6",
    "description": "string",
    "created_at": "2025-10-06T22:54:19.955358Z"
  },
  {
    "id": 2,
    "user_name": "kakakaf6",
    "description": "string",
    "created_at": "2025-10-06T22:54:19.851303Z"
  }]

**GET /applications с фильтром**

* Ввод: Параметры `page` 1, `size` 3, `user_name` mark.
* Действие: Получить список приложений по фильтру.
* Ожидаемый результат: JSON-массив приложений только с указанным `user_name`.
* ```
  [{
    "id": 15,
    "user_name": "mark",
    "description": "big deal man",
    "created_at": "2025-10-06T23:13:12.483490Z"
  },
  {
    "id": 14,
    "user_name": "mark",
    "description": "big deal man",
    "created_at": "2025-10-06T23:13:12.350125Z"
  },
  {
    "id": 13,
    "user_name": "mark",
    "description": "big deal man",
    "created_at": "2025-10-06T23:13:12.222920Z"
  }]

---

## 3. Запуск тестов

Тесты находятся в папке `tests`.

```bash
pytest -v
```

* Используются `pytest`, `pytest-asyncio`, `unittest.mock`.
* Проверяются сервис, провайдер и KafkaPublisher.

---

## 4. Структура проекта

```
app/             # Основной код приложения
  migrations/    # Миграции БД
  config.py      # Настройки
  database.py    # Подключение к БД
  kafka_publisher.py # Kafka producer
  logger.py      # Логгер
  main.py        # Точка входа
  models.py      # SQLAlchemy модели
  providers.py   # Dishka DI провайдер
  routes.py      # FastAPI роуты
  schemas.py     # Pydantic схемы
  services.py    # Сервисный слой
kafka_data/      # Данные Kafka 
pg_database/     # Данные PostgreSQL
tests/           # Тесты
.env.dev             # Переменные окружения
app.log          # Лог приложения
docker-compose.yml
Dockerfile
requirements.txt
README.md
```
