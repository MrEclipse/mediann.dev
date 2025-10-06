import json
from aiokafka import AIOKafkaProducer, errors
from app.config import settings
from app.logger import logger
from typing import Optional

"""Singleton Kafka publisher с асинхронным start/stop и отправкой сообщений"""


class KafkaPublisher:
    _instance: Optional["KafkaPublisher"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._producer: Optional[AIOKafkaProducer] = None
        self._started = False

    async def start(self):
        if not self._started:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            try:
                await self._producer.start()
                self._started = True
                logger.info("KafkaProducer запущен")
            except errors.KafkaError as e:
                logger.exception("Ошибка запуска KafkaProducer")
                raise

    async def stop(self):
        if self._producer and self._started:
            try:
                await self._producer.stop()
                logger.info("KafkaProducer остановлен")
            except errors.KafkaError:
                logger.exception("Ошибка остановки KafkaProducer")
            finally:
                self._producer = None
                self._started = False

    async def publish(self, topic: str, value: dict):
        if not self._started:
            await self.start()
        try:
            await self._producer.send_and_wait(topic, value)
            logger.info("Сообщение отправлено в Kafka", extra={"topic": topic, "value": value})
        except errors.KafkaError:
            logger.exception(f"Ошибка при отправке сообщения в Kafka topic={topic}")
