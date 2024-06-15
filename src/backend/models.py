import time

from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, BigInteger, String, create_engine
from src.backend import DATABASE_URL
from src.backend.logger import logger

time.sleep(3)

engine = create_engine(DATABASE_URL)
Base = declarative_base()
metadata = Base.metadata


class Memes(Base):
    __tablename__ = "memes"

    id = Column(BigInteger, primary_key=True, nullable=False)
    minio_path = Column(String, nullable=False, unique=True)
    text = Column(String, nullable=False)


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)


@contextmanager
def SessionManager() -> Session:
    session = SessionLocal()
    try:
        yield session
    except Exception as ex:
        logger.error(f"SessionManager() error: {ex}")
        session.rollback()
    finally:
        session.close()
