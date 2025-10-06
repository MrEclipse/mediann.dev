import pytest
from unittest.mock import AsyncMock, patch
from app.kafka_publisher import KafkaPublisher


@pytest.mark.asyncio
async def test_kafka_start_and_stop():
    """Тестирует запуск и остановку KafkaPublisher"""
    mock_producer = AsyncMock()
    with patch("app.kafka_publisher.AIOKafkaProducer", return_value=mock_producer):
        kafka = KafkaPublisher()
        await kafka.start()
        mock_producer.start.assert_awaited_once()
        assert kafka._started
        await kafka.stop()
        mock_producer.stop.assert_awaited_once()
        assert not kafka._started


@pytest.mark.asyncio
async def test_kafka_publish(monkeypatch):
    """Тестирует публикацию сообщения через KafkaPublisher"""
    kafka = KafkaPublisher()
    fake_producer = AsyncMock()
    monkeypatch.setattr(kafka, "_producer", fake_producer)
    kafka._started = True

    await kafka.publish("test-topic", {"msg": "hello"})
    fake_producer.send_and_wait.assert_awaited_once()
