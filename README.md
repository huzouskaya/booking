# 🏫 Система бронирования аудиторий и оборудования

Веб-приложение для управления бронированием ресурсов учебного заведения: аудиторий, компьютерных классов, лабораторий, переговорных комнат и оборудования.

## 📋 Оглавление

- [Описание проекта](#-описание-проекта)
- [Функциональные возможности](#-функциональные-возможности)
- [Технологии](#-технологии)
- [Установка и запуск](#-установка-и-запуск)
- [API Документация](#-api-документация)
- [Структура базы данных](#-структура-базы-данных)
- [Роли пользователей](#-роли-пользователей)
- [Примеры запросов](#-примеры-запросов)
- [Деплой](#-деплой)
- [Лицензия](#-лицензия)

## 🎯 Описание проекта

Система предназначена для эффективного распределения ограниченных ресурсов учебного заведения. Пользователи могут просматривать доступные помещения и оборудование, бронировать их на выбранные дату и время, а также отслеживать статус своих заявок.

**Актуальность:** Учебные заведения часто сталкиваются с проблемой неэффективного распределения аудиторий и оборудования. Данная система решает эту проблему, предоставляя удобный онлайн-интерфейс для бронирования ресурсов.

### Основные возможности

- ✅ Просмотр каталога ресурсов с фильтрацией по категориям
- ✅ Бронирование ресурсов с проверкой доступности
- ✅ Учёт уникальных объектов (аудитории) и множественных (оборудование)
- ✅ Управление статусами бронирований
- ✅ Ролевая модель доступа (гость, пользователь, преподаватель, администратор)
- ✅ Административная панель для управления ресурсами и заявками
- ✅ JWT-аутентификация
- ✅ Swagger/ReDoc документация API

## 🛠 Технологии

### Backend
| Технология | Версия | Назначение |
|------------|--------|------------|
| Python | 3.11+ | Язык программирования |
| Django | 5.0.6 | Веб-фреймворк |
| Django REST Framework | 3.15.1 | Создание REST API |
| Simple JWT | 5.3.1 | JWT-аутентификация |
| PostgreSQL | 15+ | База данных |
| Django CORS Headers | 4.3.1 | CORS для фронтенда |
| django-filter | 24.2 | Фильтрация данных |
| drf-yasg | 1.21.7 | Swagger-документация |
| Pillow | 10.3.0 | Работа с изображениями |

### Frontend (планируется)
- **Vue 3** — современный фронтенд-фреймворк
- **Vite** — сборка проекта
- **Pinia** — управление состоянием
- **Vue Router** — маршрутизация
- **Axios** — HTTP-клиент

## 🚀 Установка и запуск

### Предварительные требования

- Python 3.11 или выше
- PostgreSQL 15 или выше
- Git
- pip (менеджер пакетов Python)

### Пошаговая инструкция

#### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/booking-system.git
cd booking-system
```

#### 2. Создание виртуального окружения

```bash
python -m venv venv

# Активация:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

#### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 4. Настройка базы данных PostgreSQL

Создайте базу данных и пользователя:

```sql
CREATE DATABASE booking_system;
CREATE USER booking_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE booking_system TO booking_user;
```

#### 5. Настройка переменных окружения

Создайте файл `.env` в корневой директории:

```env
# Django
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True

# Database
DATABASE_URL=postgresql://booking_user:secure_password_here@localhost:5432/booking_system

# Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# Frontend URLs (для CORS)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### 6. Выполнение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Создание суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

Заполните поля:
- Username: admin
- Email: admin@example.com
- Password: admin123 (или свой пароль)

#### 8. Заполнение тестовыми данными (опционально)

Создайте файл `fixtures/initial_data.json`:

```json
[
  {
    "model": "bookings.category",
    "pk": 1,
    "fields": {
      "name": "Аудитории",
      "slug": "auditorii",
      "description": "Учебные аудитории для проведения занятий",
      "icon": "classroom"
    }
  },
  {
    "model": "bookings.category",
    "pk": 2,
    "fields": {
      "name": "Компьютерные классы",
      "slug": "kompyuternye-klassy",
      "description": "Компьютерные классы с доступом к интернету",
      "icon": "computer"
    }
  },
  {
    "model": "bookings.resource",
    "pk": 1,
    "fields": {
      "name": "Аудитория 666",
      "description": "Большая аудитория на 100 мест с проектором",
      "category": 1,
      "total_quantity": 1,
      "location": "Корпус 6, этаж 6",
      "is_active": true
    }
  }
]
```

Загрузите данные:

```bash
python manage.py loaddata fixtures/initial_data.json
```

#### 9. Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://localhost:8000`

#### 10. Доступ к документации API

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **Админка**: `http://localhost:8000/admin/` (логин: admin, пароль: admin123)

## 📊 API Документация

### Пользователи

| Метод | Эндпоинт | Описание | Доступ |
|-------|----------|----------|--------|
| POST | `/api/v1/users/register/` | Регистрация нового пользователя | Все |
| POST | `/api/v1/users/token/` | Получение JWT токена (вход) | Все |
| POST | `/api/v1/users/token/refresh/` | Обновление JWT токена | Все |
| GET | `/api/v1/users/token/verify/` | Проверка JWT токена | Все |
| GET | `/api/v1/users/profile/` | Получение профиля пользователя | Авторизованные |
| PUT/PATCH | `/api/v1/users/profile/` | Обновление профиля пользователя | Авторизованные |

### Категории

| Метод | Эндпоинт | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/bookings/categories/` | Список всех категорий | Все |
| POST | `/api/v1/bookings/categories/` | Создание категории | Администратор |
| GET | `/api/v1/bookings/categories/{id}/` | Детальная информация о категории | Все |
| PUT/PATCH | `/api/v1/bookings/categories/{id}/` | Обновление категории | Администратор |
| DELETE | `/api/v1/bookings/categories/{id}/` | Удаление категории | Администратор |

### Ресурсы

| Метод | Эндпоинт | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/bookings/resources/` | Список всех ресурсов | Все |
| POST | `/api/v1/bookings/resources/` | Создание ресурса | Администратор |
| GET | `/api/v1/bookings/resources/{id}/` | Детальная информация о ресурсе | Все |
| PUT/PATCH | `/api/v1/bookings/resources/{id}/` | Обновление ресурса | Администратор |
| DELETE | `/api/v1/bookings/resources/{id}/` | Удаление ресурса | Администратор |

**Параметры фильтрации для ресурсов:**
- `category` — фильтр по ID категории
- `is_active` — фильтр по активности (true/false)
- `is_unique` — фильтр по уникальности (true/false)
- `search` — поиск по названию и описанию

### Проверка доступности

| Метод | Эндпоинт | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/bookings/check-availability/` | Проверка доступности ресурса | Все |

**Параметры запроса:**
- `resource_id` (обязательный) — ID ресурса
- `date` (обязательный) — Дата в формате YYYY-MM-DD
- `start_time` (обязательный) — Время начала в формате HH:MM
- `end_time` (обязательный) — Время окончания в формате HH:MM
- `quantity` (опциональный) — Количество экземпляров (по умолчанию 1)

**Пример ответа:**
```json
{
  "is_available": true,
  "message": "Доступно",
  "available_count": 5
}
```

### Бронирования

| Метод | Эндпоинт | Описание | Доступ |
|-------|----------|----------|--------|
| GET | `/api/v1/bookings/` | Список бронирований | Авторизованные |
| POST | `/api/v1/bookings/` | Создание бронирования | Авторизованные |
| GET | `/api/v1/bookings/{id}/` | Детальная информация о бронировании | Авторизованные |
| PUT/PATCH | `/api/v1/bookings/{id}/` | Обновление бронирования (только статус) | Администратор |
| DELETE | `/api/v1/bookings/{id}/` | Удаление бронирования | Владелец |
| POST | `/api/v1/bookings/{id}/cancel/` | Отмена бронирования | Владелец |

**Параметры фильтрации для бронирований:**
- `status` — фильтр по статусу (pending, confirmed, rejected, completed, cancelled)
- `date` — фильтр по дате (YYYY-MM-DD)
- `resource` — фильтр по ID ресурса

**Статусы бронирований:**
- `pending` — Ожидает подтверждения
- `confirmed` — Подтверждено
- `rejected` — Отклонено
- `completed` — Завершено
- `cancelled` — Отменено пользователем

## 🗄 Структура базы данных

### Схема таблиц

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│      users      │     │   categories    │     │    resources    │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │◄────│ id (PK)         │
│ username        │     │ name            │     │ name            │
│ password        │     │ slug            │     │ description     │
│ email           │     │ description     │     │ category_id (FK)│
│ first_name      │     │ icon            │     │ total_quantity  │
│ last_name       │     │ created_at      │     │ image           │
│ phone           │     └─────────────────┘     │ is_active       │
│ department      │                             │ location        │
│ position        │     ┌─────────────────┐     │ specifications  │
│ is_staff        │     │ user_profiles   │     │ created_at      │
│ is_active       │     ├─────────────────┤     │ updated_at      │
│ ...             │     │ id (PK)         │     └─────────────────┘
└─────────────────┘     │ user_id (FK)    │              │
        │               │ role            │              │
        │               │ avatar          │              │
        │               └─────────────────┘              │
        └────────────────────────────────────────────────┘
                         │
                         ▼
              ┌────────────────────────────────┐
              │          bookings              │
              ├────────────────────────────────┤
              │ id (PK)                        │
              │ user_id (FK → users.id)        │
              │ resource_id (FK → resources.id)│
              │ date (DATE)                    │
              │ start_time (TIME)              │
              │ end_time (TIME)                │
              │ quantity (INT)                 │
              │ status (VARCHAR(20))           │
              │ comment (TEXT)                 │
              │ admin_comment (TEXT)           │
              │ created_at (TIMESTAMP)         │
              │ updated_at (TIMESTAMP)         │
              └────────────────────────────────┘
```

### Индексы для оптимизации

```sql
-- Ускорение поиска по времени
CREATE INDEX idx_bookings_resource_time 
ON bookings(resource_id, date, start_time, end_time);

-- Ускорение поиска по пользователю и статусу
CREATE INDEX idx_bookings_user_status 
ON bookings(user_id, status);
```

## 👥 Роли пользователей

| Роль | Права доступа |
|------|---------------|
| **Гость** (неавторизованный) | • Просмотр главной страницы<br>• Просмотр списка ресурсов<br>• Просмотр карточек ресурсов<br>❌ Не может бронировать |
| **Пользователь** | • Все права гостя<br>• Создание бронирований<br>• Просмотр своих бронирований<br>• Отмена своих бронирований<br>• Редактирование профиля |
| **Преподаватель** | • Все права пользователя<br>• Расширенные возможности бронирования<br>• Бронирование для занятий и мероприятий |
| **Администратор** | • Все права преподавателя<br>• Управление ресурсами (CRUD)<br>• Управление категориями (CRUD)<br>• Просмотр всех бронирований<br>• Подтверждение/отклонение заявок<br>• Изменение статусов бронирований |

## 📝 Примеры запросов

### 1. Регистрация пользователя

```bash
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivan_ivanov",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "email": "ivan@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "phone": "+375291234567",
    "department": "Факультет информатики",
    "position": "Студент",
    "role": "user"
  }'
```

**Ответ:**
```json
{
  "user": {
    "id": 1,
    "username": "ivan_ivanov",
    "email": "ivan@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "phone": "+375291234567",
    "department": "Факультет информатики",
    "position": "Студент",
    "role": "user"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. Вход в систему (получение токена)

```bash
curl -X POST http://localhost:8000/api/v1/users/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivan_ivanov",
    "password": "SecurePassword123!"
  }'
```

**Ответ:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Получение списка ресурсов с фильтрацией

```bash
curl -X GET "http://localhost:8000/api/v1/bookings/resources/?category=1&is_active=true&search=аудитория" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 4. Проверка доступности ресурса

```bash
curl -X GET "http://localhost:8000/api/v1/bookings/check-availability/?resource_id=1&date=2024-12-31&start_time=10:00&end_time=12:00&quantity=1"
```

**Ответ (доступно):**
```json
{
  "is_available": true,
  "message": "Доступно",
  "available_count": 5
}
```

**Ответ (недоступно):**
```json
{
  "is_available": false,
  "message": "Доступно только 0 из 1 запрошенных",
  "available_count": 0
}
```

### 5. Создание бронирования

```bash
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resource": 1,
    "date": "2024-12-31",
    "start_time": "10:00",
    "end_time": "12:00",
    "quantity": 1,
    "comment": "Для проведения лекции по программированию"
  }'
```

**Ответ (успешно):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "ivan_ivanov",
    "email": "ivan@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "phone": "+375291234567",
    "department": "Факультет информатики",
    "position": "Студент",
    "role": "user"
  },
  "resource": {
    "id": 1,
    "name": "Аудитория 666",
    "description": "Большая аудитория на 100 мест с проектором",
    "category": {
      "id": 1,
      "name": "Аудитории",
      "slug": "auditorii",
      "description": "Учебные аудитории для проведения занятий",
      "icon": "classroom",
      "created_at": "2024-01-01T10:00:00Z"
    },
    "total_quantity": 1,
    "image": null,
    "is_active": true,
    "location": "Корпус 6, этаж 6",
    "specifications": {},
    "is_unique": true,
    "created_at": "2024-01-01T10:00:00Z"
  },
  "date": "2024-12-31",
  "start_time": "10:00:00",
  "end_time": "12:00:00",
  "quantity": 1,
  "status": "pending",
  "comment": "Для проведения лекции по программированию",
  "admin_comment": "",
  "created_at": "2024-12-01T15:30:00Z",
  "updated_at": "2024-12-01T15:30:00Z"
}
```

**Ответ (ошибка при недоступности):**
```json
{
  "resource": [],
  "date": [],
  "start_time": [],
  "end_time": [],
  "non_field_errors": [
    "Доступно только 0 из 1 запрошенных"
  ]
}
```

### 6. Получение своих бронирований

```bash
curl -X GET http://localhost:8000/api/v1/bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Отмена бронирования

```bash
curl -X POST http://localhost:8000/api/v1/bookings/1/cancel/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Ответ:**
```json
{
  "message": "Бронирование отменено",
  "booking": {
    "id": 1,
    "user": {...},
    "resource": {...},
    "date": "2024-12-31",
    "start_time": "10:00:00",
    "end_time": "12:00:00",
    "quantity": 1,
    "status": "cancelled",
    "comment": "Для проведения лекции по программированию",
    "admin_comment": "",
    "created_at": "2024-12-01T15:30:00Z",
    "updated_at": "2024-12-01T16:00:00Z"
  }
}
```

### 8. Администратор: подтверждение бронирования

```bash
curl -X PATCH http://localhost:8000/api/v1/bookings/1/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed",
    "admin_comment": "Бронирование подтверждено"
  }'
```

### 9. Администратор: создание ресурса

```bash
curl -X POST http://localhost:8000/api/v1/bookings/resources/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Проектор Epson 13",
    "description": "Проектор для презентаций, разрешение 4K",
    "category_id": 5,
    "total_quantity": 3,
    "location": "Корпус 3, этаж 2",
    "specifications": {
      "resolution": "3840x2160",
      "brightness": "4000 люмен",
      "weight": "3.5 кг"
    },
    "is_active": true
  }'
```

## 🚢 Деплой

### Настройка для продакшена

#### 1. Измените переменные окружения

```env
DEBUG=False
SECRET_KEY=новый-секретный-ключ-минимум-50-символов
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_HOSTS=ваш-домен.com,www.ваш-домен.com
```

#### 2. Соберите статические файлы

```bash
python manage.py collectstatic --noinput
```

#### 3. Настройка Gunicorn

Создайте файл `gunicorn.conf.py`:

```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
timeout = 120
preload_app = True
```

#### 4. Настройка Nginx

```nginx
server {
    listen 80;
    server_name ваш-домен.com;

    location /static/ {
        alias /путь/к/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /путь/к/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

#### 5. Настройка SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ваш-домен.com
```

### Docker (опционально)

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Сборка статики
RUN python manage.py collectstatic --noinput

# Запуск приложения
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: booking_system
      POSTGRES_USER: booking_user
      POSTGRES_PASSWORD: secure_password_here
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U booking_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    environment:
      DATABASE_URL: postgresql://booking_user:secure_password_here@db:5432/booking_system
      DEBUG: "False"
      SECRET_KEY: ${SECRET_KEY}
      ALLOWED_HOSTS: localhost,127.0.0.1
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8000:8000"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### Запуск через Docker

```bash
# Сборка и запуск
docker-compose up -d --build

# Выполнение миграций
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Просмотр логов
docker-compose logs -f web
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
python manage.py test

# Запуск тестов конкретного приложения
python manage.py test bookings
python manage.py test users

# Запуск тестов с покрытием
pip install coverage
coverage run manage.py test
coverage report -m
coverage html  # создаст htmlcov/index.html
```

## 🔧 Устранение неполадок

### Проблема: Ошибка подключения к базе данных

```bash
# Проверьте, запущен ли PostgreSQL
sudo systemctl status postgresql

# Проверьте настройки в .env
cat .env | grep DATABASE_URL

# Проверьте доступность БД
psql -U booking_user -h localhost -d booking_system
```

### Проблема: Ошибка миграций

```bash
# Откат последней миграции
python manage.py migrate bookings zero

# Удаление проблемных миграций
rm bookings/migrations/00*.py

# Создание заново
python manage.py makemigrations bookings
python manage.py migrate
```

### Проблема: CORS ошибка при работе с фронтендом

Убедитесь, что в `settings.py` добавлен ваш фронтенд-адрес:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # React
    "https://ваш-домен.com",
]
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функциональности:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Зафиксируйте изменения:
   ```bash
   git commit -m 'feat: добавить потрясающую функциональность'
   ```
4. Отправьте изменения:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Откройте Pull Request

### Стиль кода

- **PEP 8** — стиль оформления Python кода
- **Black** — автоматическое форматирование
- **isort** — сортировка импортов
- **flake8** — проверка стиля

```bash
# Установка инструментов
pip install black isort flake8

# Форматирование
black .
isort .

# Проверка
flake8
```

### Соглашения по коммитам

- `feat:` — новая функциональность
- `fix:` — исправление бага
- `docs:` — изменения в документации
- `style:` — изменения в оформлении кода
- `refactor:` — рефакторинг
- `perf:` — улучшение производительности
- `test:` — добавление/изменение тестов
- `chore:` — обслуживание проекта

## 📄 Лицензия

MIT License

Copyright (c) 2024 huzouskaya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 📧 Контакты

- **Автор**: Гузовская Александра
- **Email**: huzouskayaaliaksandra@gmail.com
- **Telegram**: @suddenly_registered

## 🙏 Благодарности

- Django REST Framework за отличный инструментарий
- PostgreSQL за надёжную работу с данными

**⭐ Если вам понравился проект, поставьте звезду на GitHub!**
