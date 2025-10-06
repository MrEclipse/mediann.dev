import sys
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine, pool

# Добавляем корень проекта в sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from models import Base  # SQLAlchemy Base
from config import settings  # Настройки

# Метаданные для автогенерации миграций
target_metadata = Base.metadata

def run_migrations_online():
    # Для Alembic нужен синхронный драйвер
    url = settings.DATABASE_URL.replace("asyncpg", "psycopg2")
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Чтобы Alembic работал с 'autogenerate'
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise RuntimeError("Offline migrations not supported with async setup")
else:
    run_migrations_online()
