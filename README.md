# Запуск
Для зспуска потребуется установленный докер и прописать в cmd/terminal: 

`docker compose up --build` || `docker-compose up --build`

# Функционал

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
