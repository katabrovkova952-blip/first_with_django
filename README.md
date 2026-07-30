# BookShelf API
![CI](https://github.com/katabrovkova952-blip/first_with_django/actions/workflows/tests.yml/badge.svg)

🔗 **Live demo:** https://first-with-django.onrender.com/api/docs/

Backend REST API для персональної бібліотеки книг: облік прочитаних і бажаних книг, відстеження прогресу читання, відгуки.

Навчальний pet-проєкт.

## Стек

- Python, Django, Django REST Framework
- PostgreSQL
- JWT-автентифікація (djangorestframework-simplejwt)
- pytest, pytest-django (fixtures, parametrize, тести на права доступу та IDOR)
- Docker, docker-compose
- drf-spectacular (автогенерована OpenAPI/Swagger документація)
- django-filter (фільтрація та пошук)

## Функціонал

- Реєстрація користувачів та авторизація через JWT
- CRUD для книг: перегляд доступний всім, створення/редагування/видалення — тільки для staff-користувачів
- Особиста полиця (Shelf) користувача: додавання книги, статус читання ("хочу прочитати" / "читаю" / "прочитано"), відстеження поточної сторінки
- Відгуки (Review): можна залишити тільки після завершення книги і тільки на власну книгу
- Фільтрація, пошук і сортування списку книг (автор, рік, назва)
- Пагінація списків
- Приватність даних користувача: чужі записи на полиці/відгуки повертають 404, а не 403 (щоб не розкривати сам факт їх існування)

## Запуск проєкту

Проєкт запускається через Docker — окремо встановлювати Python, PostgreSQL тощо не потрібно.

1. Склонувати репозиторій:
   ```bash
   git clone https://github.com/katabrovkova952-blip/first_with_django
   cd bookshelf
   ```

2. Створити файл `.env` в корені проєкту:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=bookshelf
   DB_USER=bookshelf
   DB_PASSWORD=bookshelf
   DB_HOST=db
   DB_PORT=5432
   ```

3. Зібрати та запустити контейнери:
   ```bash
   docker-compose up --build
   ```

4. У новому терміналі застосувати міграції:
   ```bash
   docker-compose exec bookshelf python manage.py migrate
   ```

5. (опційно) створити суперкористувача для доступу до адмінки:
   ```bash
   docker-compose exec bookshelf python manage.py createsuperuser
   ```

Проєкт буде доступний на **http://localhost:8000/**

## API-документація

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI-схема (JSON): http://localhost:8000/api/schema/

## Тестування

```bash
docker-compose exec bookshelf pytest
```

Тести покривають: авторизацію, розмежування прав (звичайний користувач / staff), валідацію вхідних даних, приватність чужих записів (IDOR), бізнес-логіку полиці та відгуків.

## Основні ендпоінти

| Метод | URL | Опис |
|---|---|---|
| POST | `/api/register/` | Реєстрація нового користувача |
| POST | `/api/token/` | Отримати JWT-токен (access + refresh) |
| POST | `/api/token/refresh/` | Оновити access-токен |
| GET, POST | `/api/books/` | Список книг / створення книги (тільки staff) |
| GET, PATCH, DELETE | `/api/books/{id}/` | Деталі, редагування, видалення книги |
| GET, POST | `/api/shelf/` | Полиця поточного користувача |
| GET, PATCH, DELETE | `/api/shelf/{id}/` | Запис на полиці |
| GET, POST | `/api/review/` | Відгуки |

## Автор

Катерина — https://github.com/katabrovkova952-blip · www.linkedin.com/in/kateryna-brovkova256444410
