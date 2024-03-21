<br>

<div id="header" align="center">
  <img src="https://img.shields.io/badge/Python-3.12.2-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/PostgreSQL-555555?style=for-the-badge&logo=postgresql&logoColor=F5F5DC">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green">
  <img src="https://img.shields.io/badge/Docker-555555?style=for-the-badge&logo=docker&logoColor=2496ED">
</div>

<br>

Документация к API будет доступна по url-адресу [PAY2U/SWAGER]()

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

  ```


Находясь в корневой папке проекта выполните миграции.
  ```
  python manage.py migrate
  ```

Для запуска сервера используйте данную команду:
  ```
  python manage.py runserver
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
  ```
- Из папки **infra** запустите docker-compose-prod.yaml:
  ```
  ~$ docker-compose up -d --build
  ```
- В контейнере **backend** выполните миграции:
  ```
  ~$ docker-compose exec backend python manage.py migrate

  ~$ docker-compose exec backend python manage.py collectstatic

  ~$ docker-compose exec backend backend cp -r /app/collected_static/. /backend_static/static/
  ```

Документация к API будет доступна по url-адресу [127.0.0.1/redoc](http://127.0.0.1/redoc)

</details>

<details><summary>Ссылки на используемые библиотеки</summary>

- [Python](https://www.python.org/downloads/release/python-3122/)
- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)

</details>

* **Разработчики Backend:**
  + [Василий](https://github.com/inferno681)
  + [Александр](https://github.com/abaz47)
