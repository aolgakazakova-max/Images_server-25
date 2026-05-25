# Image Server (Flask + Nginx + Docker)
##  Описание

Image Server — это сервис для загрузки, хранения и раздачи изображений.  
Архитектура включает Flask-приложение, Nginx в роли reverse proxy и Docker Compose для оркестрации.



## Технологии

- Python 3.12
- Flask
- Nginx 1.27 (alpine)
- Docker & Docker Compose
- Pillow (PIL)



## Архитектура
Browser
↓
Nginx (http://localhost:8080)
↓
Flask App (app:3000)
↓
Docker Volumes (images, logs)




## Запуск проекта

### 1. Сборка и запуск

docker-compose up -d --build

## Остановка

docker-compose down

## Доступ к приложению
## Главная страница:
http://localhost:8080/
## Страница загрузки:
http://localhost:8080/upload
## Список изображений:
http://localhost:8080/images/
## Прямой доступ к изображению:
http://localhost:8080/images/<filename>
## Загрузка изображения

POST /upload

Параметры:
image — файл (JPG, PNG, GIF)
Пример ответа:
{
  "message": "OK",
  "id": "file_name.png",
  "url": "/images/file_name.png",
  "full_url": "http://localhost:8080/images/file_name.png"
}
## Удаление изображения

POST /delete/<filename>

Ответ:
{
  "message": "deleted"
}
## Хранение данных

## Используются Docker volumes:

images/ — загруженные изображения
logs/ — логи приложения
## Ограничения
Максимальный размер файла: 5 MB
Поддерживаемые форматы:
JPG
PNG
GIF
## Проверка работы

## Открыть:

http://localhost:8080/
## Загрузить изображение через /upload

## Проверить доступ:

http://localhost:8080/images/<filename>
##  Логи

## Логи сохраняются в:

/logs/app.log



