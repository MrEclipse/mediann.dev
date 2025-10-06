from fastapi import APIRouter, Query
from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from app.schemas import ApplicationCreate, ApplicationRead
from app.services import ApplicationService

"""API маршруты: создание и список приложений"""

router = APIRouter(route_class=DishkaRoute)


@router.post("/applications", response_model=ApplicationRead)
@inject
async def create_application(
        application_data: ApplicationCreate,
        service: FromDishka[ApplicationService],
):
    """Создание нового приложения"""
    return await service.create_application(application_data)


@router.get("/applications", response_model=list[ApplicationRead])
@inject
async def list_applications(
        service: FromDishka[ApplicationService],
        page: int = 1,
        size: int = 20,
        user_name: str | None = Query(default=None, description="Filter by user_name"),
):
    """Получение списка приложений"""
    apps, _ = await service.get_applications(page, size, user_name)
    return apps
