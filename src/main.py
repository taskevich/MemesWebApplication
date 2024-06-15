import io
import os
import uuid

from fastapi import FastAPI, File, UploadFile
from sqlalchemy import func, text

from src.backend.models import SessionManager, Memes
from src.backend.schemas import UpdateMemeResponse, MemesResponse, MemeResponse, MemeItem, AddMemeResponse, \
    DeleteMemeResponse
from src.backend import minio_client, BUCKET_NAME
from src.backend.utils import run_parallel
from src.backend.logger import logger

app = FastAPI()


@app.on_event("startup")
def startup():
    """
        Инициализация
    """
    logger.info("Initialization application")
    try:
        if not minio_client.bucket_exists(BUCKET_NAME):
            minio_client.make_bucket(BUCKET_NAME)
            logger.info("S3-bucket memes was created")
    except Exception as ex:
        logger.error(f"Error fastapi initialization: {ex}")


@app.get("/memes", response_model=MemesResponse)
def get_memes(limit: int = 20, offset: int = 0, sort: str = "asc"):
    """
        Список мемов
    """
    with SessionManager() as session:
        memes_query = session.query(Memes) \
            .order_by(text(f"id {sort}")) \
            .limit(limit).offset(offset).all
        memes_count_query = session.query(func.count(Memes.id)).scalar

        memes, memes_count = run_parallel(memes_query, memes_count_query)

        return MemesResponse(
            totalCount=memes_count,
            payload=[
                MemeItem(
                    id=meme_element.id,
                    path=meme_element.minio_path,
                    text=meme_element.text
                )
                for meme_element in memes
            ]
        )


@app.get("/memes/{meme_id}", response_model=MemeResponse)
def get_concrete_meme(meme_id: str):
    """
        Получение всех мемов
    """
    with SessionManager() as session:
        meme: Memes = session.query(Memes).filter(Memes.id == meme_id).first()

        if not meme:
            return DeleteMemeResponse(error=True, message="Мем не найден")

        return MemeResponse(
            payload=MemeItem(
                id=meme.id,
                path=meme.minio_path,
                text=meme.text
            )
        )


@app.post("/memes", response_model=AddMemeResponse)
def add_meme(text: str, image: UploadFile = File(...)):
    """
        Добавление мема
    """
    with SessionManager() as session:
        try:
            if not text:
                return UpdateMemeResponse(error=True, message="Пустое описание мема")

            _, ext = os.path.splitext(image.filename)

            if not ext:
                return UpdateMemeResponse(error=True, message="Неизвестное расширение файла")

            data = io.BytesIO(image.file.read())
            path = f"{uuid.uuid4()}{ext}"
            minio_client.put_object(
                BUCKET_NAME,
                path,
                data=data,
                length=data.getbuffer().nbytes,
            )

            meme: Memes = Memes(
                minio_path=path,
                text=text
            )
            session.add(meme)
            session.commit()
            return AddMemeResponse(message="Мем добавлен")
        except Exception as ex:
            logger.error(f"Error to add meme: {ex}")
            return AddMemeResponse(error=False, message="Не удалось добавить мем")


@app.put("/memes/{meme_id}", response_model=UpdateMemeResponse)
def update_meme(meme_id: int, text: str, image: UploadFile = File(...)):
    """
        Обновление мема
    """
    with SessionManager() as session:
        try:
            meme: Memes = session.query(Memes).filter(Memes.id == meme_id).first()

            if not meme:
                return UpdateMemeResponse(error=True, message="Мем не найден")

            if not text:
                return UpdateMemeResponse(error=True, message="Пустое описание мема")

            _, ext = os.path.splitext(image.filename)
            if not ext:
                return UpdateMemeResponse(error=True, message="Неизвестное расширение файла")

            data = io.BytesIO(image.file.read())
            minio_client.put_object(
                BUCKET_NAME,
                meme.minio_path,
                data=data,
                length=data.getbuffer().nbytes,
            )

            meme.text = text
            session.commit()
            return UpdateMemeResponse()
        except Exception as ex:
            logger.error(f"Error to update meme: {ex}")
            return UpdateMemeResponse(error=True, message="Не удалось обновить мем")


@app.delete("/memes/{meme_id}", response_model=DeleteMemeResponse)
def delete_meme(meme_id: int):
    """
        Удаление мема
    """
    with SessionManager() as session:
        meme: Memes = session.query(Memes).filter(Memes.id == meme_id).first()
        if not meme:
            return DeleteMemeResponse(error=True, message="Мем не найден")
        session.delete(meme)
        session.commit()
    return DeleteMemeResponse(message="Мем удален")
