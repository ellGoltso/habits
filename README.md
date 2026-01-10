# Habit Tracker API

Современное веб-приложение для отслеживания полезных привычек. Система мотивирует пользователей, отправляя своевременные уведомления в Telegram и предоставляя доступ к базе публичных привычек.

## 🚀 Основные возможности
- **Управление привычками:** Полный CRUD для личных привычек.
- **Публичный каталог:** Просмотр привычек других пользователей.
- **Telegram-уведомления:** Интеграция с Celery для рассылки напоминаний по расписанию.
- **Умная валидация:**
  - Ограничение времени выполнения (макс. 120 секунд).
  - Контроль периодичности (минимум раз в неделю).
  - Логическая проверка: запрет на одновременный выбор вознаграждения и приятной привычки.

## 🛠 Технологический стек
- **Backend:** Python 3.13 / Django 5.1 / DRF
- **Auth:** JWT (Djoser + SimpleJWT)
- **Database:** PostgreSQL
- **Async Tasks:** Celery + Redis
- **Documentation:** OpenAPI 3.0 (drf-spectacular + Swagger)
- **CORS:** django-cors-headers

## 📦 Установка и запуск

### 1. Подготовка окружения
Клонируйте репозиторий и создайте файл `.env` в корне проекта:
```env
# Django settings
SECRET_KEY=
DEBUG=

# Database
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=

# Telegram
TELEGRAM_BOT_TOKEN=

# Celery & Redis
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
```
### 2. Установка зависимостей (Poetry)
```
poetry install
poetry shell
```
### 3.База данных и пользователи
```
python manage.py migrate
python manage.py createsuperuser
```
### 4.Запуск сервисов (в разных терминалах)
* API-сервер:
```
python manage.py runserver
```
* Celery Worker (на Windows используйте -P solo):
```
celery -A config worker -l info -P solo
```
* Celery Beat (планировщик):
```
celery -A config beat -l info
```
## 📖 Документация API
После запуска сервера документация в формате Swagger доступна по адресу:
👉 http://localhost:8000/swagger/
Авторизация: Для тестирования защищенных эндпоинтов используйте кнопку Authorize и вставьте токен в формате Bearer <ваш_token>.
## 🧪 Тестирование и покрытие
* Запуск тестов:
```
python manage.py test
```
* Отчет о покрытии:
```
coverage run --source='.' manage.py test
coverage report
```
