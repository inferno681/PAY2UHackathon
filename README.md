[![Deploy](https://github.com/inferno681/PAY2UHackathon/actions/workflows/deploy.yaml/badge.svg)](https://github.com/inferno681/PAY2UHackathon/actions/workflows/deploy.yaml)
<br>

<div id="header" align="center">
  <img src="https://img.shields.io/badge/Python-3.12.2-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/PostgreSQL-555555?style=for-the-badge&logo=postgresql&logoColor=F5F5DC">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green">
  <img src="https://img.shields.io/badge/Docker-555555?style=for-the-badge&logo=docker&logoColor=2496ED">
  <img src="https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4">
  <img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
</div>

<br>

Документация к API доступна по url-адресу [PAY2U/SWAGER](https://pay2u.ddns.net/api/schema/swagger-ui/)

<details><summary><h1>Сервис для управления подписками</h1></summary>

* **MVP:**
  + Цель: Организация управления подписками пользователя.
  + Размещение: Внутри банковского приложения.

* **Функциональные возможности:**
  + Оформление подписки на различные сервисы.
  + Мониторинг сроков оплаты.

* **Преимущества:**
  + Все подписки собраны в одном месте.
  + Отслеживание сроков продления подписки.

* **Целевая аудитория:**
  + Клиенты банковских приложений.

</details>

<details><summary><h1>Инструкция по установке</h1></summary>

Клонируйте репозиторий и перейдите в него.
```bash
git@github.com:inferno681/PAY2UHackathon.git
```

Для установки зависимостей создайте и активируйте виртульное окружение и выполните следующую команду:
```bash
pip install -r requirements.txt
```

Создайте файл **.env**, в корневой папке проекта, с переменными окружения.

```
  POSTGRES_USER=django_user (имя пользователя для СУБД)
  POSTGRES_PASSWORD=mysecretpassword (пароль пользователя для СУБД)
  POSTGRES_DB=django (имя базы данных)
  DB_HOST=db (контейнер с базой данных)
  DB_PORT=5432 (порт для PostgreSQL)
  SECRET_KEY = ... (SECRET_KEY для settings.py)
  ALLOWED_HOSTS =127.0.0.1,localhost (список разрешенных хостов)
  DEBUG=True (включение или выключение режима отладки)
  SQLITE_ACTIVATED=True (Если True, то будет использоваться SQLite вместо PostgreSQL)
  CSRF_TRUSTED_ORIGINS=(адрес сайта)
  CORS_ORIGIN_WHITELIST=http://localhost:3000 (список адресов для открытия возможности удаленного подключения)
  DOCS_TITLE=(заголовок в автодокументации)
  DOCS_DESCRIPTION=(описание в автодокументации)
  CELERY_BROKER_URL=(брокер сообщений)
  CACHES_BACKEND=(бэкэнд для кэша, подробнее https://docs.djangoproject.com/en/5.0/topics/cache/)
  CACHES_LOCATION=(место хранения кэша)
  CELERY_CACHE_BACKEND=(Кэш для celery)
  CELERY_BEAT_SCHEDULER=(Планировщик celery)

```


Находясь в корневой папке проекта выполните миграции.
  ```
  python manage.py migrate
  ```

Команда для запуска сервера:
  ```
  python manage.py runserver
  ```
Команда для запуска celery worker:
  ```
  celery -A pay2u worker -l warning
  ```
Команда для запуска celery beat:
  ```
  celery -A pay2u beat -l warning
  ```

</details>

<details><summary><h1>Запуск проекта через докер</h1></summary>

- Клонируйте репозиторий.
- Перейдите в папку **infra** и создайте в ней файл **.env** с переменными окружения:
  ```
  POSTGRES_USER=django_user (имя пользователя для СУБД)
  POSTGRES_PASSWORD=mysecretpassword (пароль пользователя для СУБД)
  POSTGRES_DB=django (имя базы данных)
  DB_HOST=db (контейнер с базой данных)
  DB_PORT=5432 (порт для PostgreSQL)
  SECRET_KEY = ... (SECRET_KEY для settings.py)
  ALLOWED_HOSTS =127.0.0.1,localhost (список разрешенных хостов)
  DEBUG=True (включение или выключение режима отладки)
  SQLITE_ACTIVATED=True (Если True, то будет использоваться SQLite вместо PostgreSQL)
  CSRF_TRUSTED_ORIGINS=(адрес сайта)
  CORS_ORIGIN_WHITELIST=http://localhost:3000 (список адресов для открытия возможности удаленного подключения)
  DOCS_TITLE=(заголовок в автодокументации)
  DOCS_DESCRIPTION=(описание в автодокументации)
  CELERY_BROKER_URL=(брокер сообщений)
  CACHES_BACKEND=(бэкэнд для кэша, подробнее https://docs.djangoproject.com/en/5.0/topics/cache/)
  CACHES_LOCATION=(место хранения кэша)
  CELERY_CACHE_BACKEND=(Кэш для celery)
  CELERY_BEAT_SCHEDULER=(Планировщик celery)
  ```
- Из папки **infra** запустите docker-compose-prod.yaml:
  ```
  ~$ docker compose -f docker-compose-prod.yaml up -d
  ```
- В контейнере **backend** выполните миграции:
  ```
  ~$ docker compose -f docker-compose-prod.yaml exec backend python manage.py migrate

  ~$ docker compose -f docker-compose-prod.yaml exec backend python manage.py collectstatic

  ~$ docker compose -f docker-compose-prod.yaml exec backend cp -r /app/collected_static/. /backend_static/static/
  ```


</details>

<details><summary>Ссылки на используемые библиотеки</summary>

- [Python](https://www.python.org/downloads/release/python-3122/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)

</details>

* **Разработчики Backend:**
  + [Василий](https://github.com/inferno681)
  + [Александр](https://github.com/abaz47)
