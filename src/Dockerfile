FROM python:3.11-buster as builder

RUN apt-get update && apt-get upgrade -y

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]