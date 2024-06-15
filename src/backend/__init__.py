import os

from minio import Minio

DATABASE_URL = os.getenv("DATABASE_URL")
MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_LOGIN = os.getenv("MINIO_LOGIN")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
BUCKET_NAME = os.getenv("BUCKET_NAME")

minio_client = Minio(
    MINIO_HOST,
    access_key=MINIO_LOGIN,
    secret_key=MINIO_PASSWORD,
    secure=False
)
