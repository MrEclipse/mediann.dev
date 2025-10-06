import pytest
from app.providers import AppProvider
from app.kafka_publisher import KafkaPublisher
from app.services import ApplicationService
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_provider_kafka_singleton():
    """Проверяет, что KafkaPublisher создаётся один раз (singleton)"""
    mock_producer = AsyncMock()
    with patch("app.kafka_publisher.AIOKafkaProducer", return_value=mock_producer):
        provider = AppProvider()
        kafka1 = await provider.kafka_publisher()
        kafka2 = await provider.kafka_publisher()
        assert kafka1 is kafka2
        assert kafka1._started


@pytest.mark.asyncio
async def test_provider_application_service():
    """Проверяет создание ApplicationService через провайдер"""
    provider = AppProvider()
    mock_db = AsyncMock()
    mock_kafka = KafkaPublisher()
    service = provider.application_service(mock_db, mock_kafka)
    assert isinstance(service, ApplicationService)
