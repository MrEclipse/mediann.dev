from unittest.mock import MagicMock, AsyncMock
import pytest
from app.schemas import ApplicationCreate
from app.services import ApplicationService


@pytest.mark.asyncio
async def test_create_application(app_service, mock_db_session):
    """Тест создания новой Application"""
    data = ApplicationCreate(user_name="TestUser", description="Demo")
    app_obj = await app_service.create_application(data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_awaited_once()
    assert app_obj.user_name == "TestUser"


@pytest.mark.asyncio
async def test_get_applications():
    """Тест получения списка Applications"""
    mock_session = AsyncMock()

    mock_total_result = MagicMock()
    mock_total_result.scalar_one.return_value = 5

    mock_scalars_result = MagicMock()
    mock_scalars_result.all.return_value = []

    mock_query_result = MagicMock()
    mock_query_result.scalars.return_value = mock_scalars_result

    mock_session.execute.side_effect = [mock_total_result, mock_query_result]

    kafka_mock = AsyncMock()
    service = ApplicationService(mock_session, kafka_mock)

    items, total = await service.get_applications()

    assert total == 5
    assert items == []
    assert mock_session.execute.await_count == 2
