from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple
from app.models import Application
from app.schemas import ApplicationCreate
from app.kafka_publisher import KafkaPublisher
from app.config import settings
from app.logger import logger

"""Сервис приложений: CRUD и Kafka события"""


class ApplicationService:
    """Логика работы с приложениями и Kafka"""

    def __init__(self, db: AsyncSession, kafka: KafkaPublisher):
        self.db = db
        self.kafka = kafka

    async def create_application(self, data: ApplicationCreate) -> Application:
        """Создание приложения и публикация события в Kafka"""
        app = Application(user_name=data.user_name, description=data.description)
        try:
            self.db.add(app)
            await self.db.commit()
            await self.db.refresh(app)
        except Exception as e:
            await self.db.rollback()
            logger.exception("Ошибка создания приложения в БД")
            raise

        try:
            await self.kafka.publish(
                settings.KAFKA_TOPIC,
                {
                    "id": app.id,
                    "user_name": app.user_name,
                    "description": app.description,
                    "created_at": str(app.created_at),
                },
            )
        except Exception:
            logger.warning("Не удалось отправить событие в Kafka, но запись в БД сохранена")

        return app

    async def get_applications(
            self, page: int = 1, size: int = 20, user_name: str | None = None
    ) -> Tuple[List[Application], int]:
        """Получение списка приложений с пагинацией, опционально фильтруя по имени"""
        from sqlalchemy import select, func

        try:
            stmt = select(Application)

            if user_name is not None:
                stmt = stmt.where(Application.user_name == user_name)

            total_stmt = select(func.count()).select_from(stmt.subquery())
            total_res = await self.db.execute(total_stmt)
            total = int(total_res.scalar_one())

            stmt = stmt.order_by(Application.created_at.desc()).offset((page - 1) * size).limit(size)
            res = await self.db.execute(stmt)
            items = res.scalars().all()

        except Exception:
            logger.exception("Ошибка получения списка приложений")
            raise

        return list(items), total
