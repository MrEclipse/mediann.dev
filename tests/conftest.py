import pytest
import os
from unittest.mock import AsyncMock, MagicMock
from app.services import ApplicationService

os.environ["ENV_FILE"] = "tests/.env.test"

from app.kafka_publisher import KafkaPublisher



@pytest.fixture
def mock_db_session():
    """Мокаем сессию SQLAlchemy"""
    mock = MagicMock()
    mock.add = MagicMock()
    mock.commit = AsyncMock()
    mock.rollback = AsyncMock()
    mock.refresh = AsyncMock()
    mock.execute = AsyncMock()
    return mock


@pytest.fixture
def mock_kafka():
    """Мокаем KafkaPublisher, чтобы не коннектился к брокеру"""
    mock = AsyncMock(spec=KafkaPublisher)
    mock.publish = AsyncMock()
    mock.start = AsyncMock()
    mock.stop = AsyncMock()
    return mock


@pytest.fixture
def app_service(mock_db_session, mock_kafka):
    """Создаёт экземпляр сервиса с замоканными зависимостями"""
    return ApplicationService(mock_db_session, mock_kafka)
