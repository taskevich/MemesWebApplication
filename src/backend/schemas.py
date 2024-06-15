from typing import Optional, Any, List

from pydantic import BaseModel


class DefaultResponse(BaseModel):
    """
        Стандартный ответ на запрос
    """
    error: Optional[bool] = False
    message: Optional[str] = "OK"
    payload: Optional[Any] = None


class MemeItem(BaseModel):
    """
        Элемент мема
    """
    id: Optional[int]
    path: Optional[str]
    text: Optional[str]


class MemesResponse(DefaultResponse):
    """
        Ответ на получение мемов
    """
    totalCount: Optional[int] = 0
    payload: Optional[List[MemeItem]] = None


class MemeResponse(DefaultResponse):
    """
        Ответ на получение конкретног мема
    """
    payload: Optional[MemeItem]


class AddMemeResponse(DefaultResponse):
    """
        Добавление мемы
    """


class DeleteMemeResponse(DefaultResponse):
    """
        Ответ на удаление мема
    """


class UpdateMemeResponse(DefaultResponse):
    """
        Ответ на запрос на обнновление мема
    """
