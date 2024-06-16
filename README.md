# Запуск
Для запуска потребуется установленный докер и прописать в cmd/terminal: 

1) `docker compose up --build` || `docker-compose up --build`
2) Зайти в minio панель и в настройках bucket `Access Policy` установить `Public`

# Функционал

- GET /memes/image/{file_name} - специальный маршрут для получения фото из bucket

- GET /memes - получения списка мемов:

`STATUS CODE == 200`
```
{
  "error": false,
  "message": "OK",
  "payload": [
    {
      "id": 0,
      "path": "string",
      "text": "string"
    }
  ],
  "totalCount": 0
}
```

- GET /memes/{meme_id} - получение конкретного мема

`STATUS_CODE == 200`

```
{
  "error": false,
  "message": "OK",
  "payload": {
    "id": 0,
    "path": "string",
    "text": "string"
  }
}
```

- POST /memes - добавление мема

`STATUS CODE == 200`
```
{
  "error": false,
  "message": "Мем добавлен",
  "payload": null
}
```

- PUT /memes/{meme_id} - Обновление мема

`STATUS CODE == 200`
```
{
  "error": false,
  "message": "OK",
  "payload": null
}
```

- DELETE /memes/{meme_id}

`STATUS CODE == 200`
```
{
  "error": false,
  "message": "OK",
  "payload": null
}
```
