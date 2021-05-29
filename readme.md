## Использование
При запросах требуется устанавливать  заголовок  “ X-API-KEY”, и в значение заголовка написать соответствующий пароль.
Сервер принимает запросы:
1. POST/pets
```
Request body
{
	“name”:  “Sunny”,
	“age”: 9,
	“type”:  “cat”
}
```

```
Response body
{
    "id": "1a3b5a88-27c9-4735-bb77-6bb68d63d546",
    "name": "Sunny",
    "age": 9,
    "type": "cat",
    "photos": [],
    "created_at": "2021-05-30T07:04:14"
}
```
2. POST/pets/{id}/photo
```
Content-type: multipart/form-data
file: binary
```
```
Response body
{
    "id": "235236ff-52c1-4e70-ac5d-4bd74a794612",
    "url": "http://address/photos/1_kyl15aC.jpg"
}
```
3. GET/pets
```
Query parameters: 
limit: integer (optional, default = 20)
offset: integer (optional, default = 0)
has_photos: boolean  (optional)
            has_photos: true - вернутся записи с фото
            has_photos:false – вернутся записи без фото
            has_photos was not provided – вернутся все записи
```
```
Response body
{
    "count": 12,
    "items": [
        {
        "id": "f0ae06c5-4213-48d3-865d-9ee5f34a4a42",
        "name": "Sunny",
        "age": 9,
        "type": "cat",
        "photos": [
                {
                "id": "51adcb35-c7d0-495c-be42-f9de18c9bee3",
                "url": "http://address/photos/1.jpg"
                }
                  ],
        "created_at": "2021-05-29T15:07:00"
        },
        {
        "id": "19868378-40bd-45d8-a78b-d6f75c295a86",
        "name": "Kek",
        "age": 1,
        "type": "cat",
        "photos": [
        ],
        "created_at": "2021-05-29T15:11:47"
        }
        ],
}
```
4. DELETE /pets
```
Request body 
{
  "ids": [
        "74c3cfca-6efe-4707-9735-6a7a9bdb80bb",
        "235236ff-52c1-4e70-ac5d-4bd74a794612"
  ]
}
```
```
Response body
{
    "deleted": 1,
    "errors": [
              {
               "id": "235236ff-52c1-4e70-ac5d-4bd74a794612",
                "error": "Pet with the matching ID was not found."
              },
              ],
}
```
## Как локально развернуть проект

1. Настройте переменные в .env.dev
2. В файле docker-compose.yml настройте переменные окружения для PostgreSQL
3. В консоли напишите команду
```
docker-compose up
```

## CLI
```
docker-compose exec web python manage.py  get_pets_command
```
Флаги:
1.  -y, --with_photos вернутся записи с фото
2.  -n, --no_with_photos вернутся записи без фото