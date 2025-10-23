# Map Test Project

Интерактивная карта мест отдыха и достопримечательностей.  
Проект реализован на **Django + DRF**, поддерживает загрузку фотографий, фильтрацию по координатам, выдачу данных в формате **GeoJSON (RFC 7946)** и документацию API через **Swagger/Redoc**.

---

## Возможности
- CRUD для мест (`Place`) и фотографий (`Photo`)
- Авторизация через JWT (SimpleJWT)
- Inline-редактирование фотографий в админке с drag-and-drop сортировкой
- Превью изображений в админке
- Поддержка WYSIWYG редактора (CKEditor5) для описаний
- Фильтрация мест по координатам (bbox)
- Эндпоинт `/api/places/geojson/` для получения FeatureCollection
- Автогенерация схемы API и документации (Swagger, Redoc)

---
## Установка и запуск

### 1. Клонирование репозитория
git clone https://github.com/Skaplich1980/Map_test.git
cd map-test
2. Создание виртуального окружения
bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
3. Установка зависимостей
bash
pip install -r requirements.txt
4. Настройка окружения
Создай файл .env в корне проекта на основе примера:

env
SECRET_KEY=django-insecure-...
DEBUG=True
DB_ENGINE=sqlite
DB_NAME=map
DB_USER=postgres
DB_PASSWORD=secret
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1

БД с примерами !
db.sqlite3  
пользователь:root
пароль:admin
если оставляем, то шаги 5-6 можно пропустить

5. Применение миграций
bash
python manage.py migrate
6. Создание суперпользователя
bash
python manage.py createsuperuser
7. Запуск сервера
bash
python manage.py runserver
?? Основные эндпоинты API
JWT авторизация

POST /api/token/ — получить токен
POST /api/token/refresh/ — обновить токен
Места
GET /api/places/ — список мест
POST /api/places/ — создать место
GET /api/places/{id}/ — детально
GET /api/places/geojson/ — все места в формате GeoJSON
Фотографии
GET /api/photos/ — список фото
POST /api/photos/ — загрузка фото
Документация API
Swagger UI: http://localhost:8000/api/docs/
Redoc: http://localhost:8000/api/redoc/
JSON-схема: http://localhost:8000/api/schema/
Админка
URL: http://localhost:8000/admin/

Возможности:
Inline-редактирование фотографий
Drag-and-drop сортировка фото
Превью изображений
Редактор CKEditor 5 для описаний мест

Статика и медиа
Статические файлы: /static/
Медиафайлы (загруженные фото): /media/

выполнение дополнительных шагов потом
Деплой на pythonanywhere / другой хостинг
Добавление команды load_place <url> для импорта данных

Загрузка тестовых данных для демонстрации

Лицензия
MIT License

проект выполнен за 4 дня, 1 день на 19,20 шаги необязательные