from typing import AsyncIterable
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.kafka_publisher import KafkaPublisher
from app.services import ApplicationService
from app.logger import logger

"""DI провайдер: DB, Kafka, ApplicationService"""


class AppProvider(Provider):
    scope = Scope.REQUEST

    _kafka_instance: KafkaPublisher | None = None

    @provide
    async def db_session(self) -> AsyncIterable[AsyncSession]:
        """Асинхронная сессия БД на запрос"""
        async with AsyncSessionLocal() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.exception("Ошибка в сессии БД")
                raise
            finally:
                await session.close()

    @provide
    async def kafka_publisher(self) -> KafkaPublisher:
        """Singleton KafkaPublisher на всё приложение"""
        if AppProvider._kafka_instance is None:
            AppProvider._kafka_instance = KafkaPublisher()
            try:
                await AppProvider._kafka_instance.start()
            except Exception as e:
                logger.exception("Ошибка при старте KafkaProducer")
                raise
        return AppProvider._kafka_instance

    @provide
    def application_service(
            self, db_session: AsyncSession, kafka_publisher: KafkaPublisher
    ) -> ApplicationService:
        """Создание сервиса ApplicationService"""
        return ApplicationService(db_session, kafka_publisher)
