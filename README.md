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
docker-compose up -d
```

Приложение будет доступно на `http://localhost:8000`.

---

## 2. Тест кейсы (Swagger)

**POST /applications**

* Ввод: JSON с `user_name` и `description`.
* Действие: Создать новое приложение.
* Ожидаемый результат: JSON с созданным приложением.
* Лог: `Сообщение отправлено в Kafka`.

**GET /applications**

* Ввод: Параметры `page` и `size`.
* Действие: Получить список приложений.
* Ожидаемый результат: JSON-массив приложений.

**GET /applications с фильтром**

* Ввод: Параметры `page`, `size`, `user_name`.
* Действие: Получить список приложений по фильтру.
* Ожидаемый результат: JSON-массив приложений только с указанным `user_name`.

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
