[![Foodgram workflow](https://github.com/KlepalovS/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/KlepalovS/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
# Foodgram. Упакован в Docker контейнеры для локального запуска.
## Приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 


Сайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Рецпту может быть присвоен тег из списка предустановленных (например, «Завтрак», «Обед» или «Ужин»). 
Добавлять теги и ингредиенты может только администратор.

## Особенности

- Самостоятельная регистрация новых пользователей через POST запрос.
- Токен получается через передачу username и email.
- Упакован в Docker контейнеры.
- Настроены CI/CD с применением GitHub Actions и автоматическим развертыванием на боевом сервере Яндекс.Облака.

## Технологии

- [Python 3.7](https://www.python.org/) - язык программирования, который позволяют быстро работать и более эффективно внедрять системы!
- [Django 3.2](https://www.djangoproject.com/) - упрощает создание лучших веб-приложений быстрее и с меньшим количеством кода.
- [Django Rest Framework 3.14.0](https://www.django-rest-framework.org/) - мощный и гибкий инструментарий для создания веб-API.
- [Docker](https://www.docker.com) - программная платформа для быстрой разработки, тестирования и развертывания приложений.
- [Nginx](https://nginx.org/ru/) - HTTP-сервер и обратный прокси-сервер, почтовый прокси-сервер, а также TCP/UDP прокси-сервер общего назначения.
- [PostgreSQL](https://www.postgresql.org) - свободная объектно-реляционная система управления базами данных.
- [React](https://react.dev) - JavaScript-библиотека с открытым исходным кодом для разработки пользовательских интерфейсов. 
- [Gunicorn](https://gunicorn.org) - HTTP-сервер с интерфейсом шлюза веб-сервера Python.
- [Яндекс.Облако](https://cloud.yandex.ru/) - публичная облачная платформа от российской интернет-компании «Яндекс». Yandex.Cloud предоставляет частным и корпоративным пользователям инфраструктуру и вычислительные ресурсы в формате as a service.
- [GitHub Actions](https://docs.github.com/ru/actions) - это облачный сервис, инструмент для автоматизации процессов тестирования и деплоя ваших проектов. Он служит тестовой площадкой, на которой можно запускать и тестировать проекты в изолированном окружении. 

##### Команда разработки:

- [Слава (в роли Python-разработчика - разработчик бекенда)](https://github.com/KlepalovS)
- [Яндекс.Практикум (в роли разработчика фронтенда)](https://practicum.yandex.ru/)

## Инструкция по локальному развертыванию проекта.

Проект упакован в четыре контейнера: frontend, nginx, PostgreSQL, gunicorn + Django.
Для локального запуска в контейнерах необходим docker, docker-compose

Клонировать репозиторий и перейти в него в командной строке.

```
git@github.com:KlepalovS/foodgram-project-react.git

foodgram-project-react/
```

Переходим в директорию с файлами для развертывания инфраструктуры. 

```
cd infra/
```

Cоздаем .env файл.

```
sudo nano .env
```

Заполняем файл по образцу ниже.

Секретный ключ Джанги.
```
SECRET_KEY='defaul_secret_key'
```
Получение/изменение SECRET_KEY (контейнер запущен).
Далее меняем в .env файле.
```
docker-compose exec backend python manage.py shell
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
Переменные режима работы сервера.
```
DEBAG='False'
```
Разрешенные хосты для подключения.
```
ALLOWED_HOSTS='localhost'
```
Переменные для настройки БД PostgreSQL в Джанго.
Движок БД. ENGINE в settings.py DATABASES.
```
DB_ENGINE=django.db.backends.postgresql
```
Задаем имя БД.
NAME в settings.py DATABASES.
```
POSTGRES_DB=postgres
```
Можно сменить БД на новую, прежде создав ее (контейнер запущен).
Далее меняем в .env файле.
```
docker-compose exec db psql -U postgres
CREATE DATABASE <db_name>
```
Задаем имя пользователя БД и пароль для этого юзера.
USER и PASSWORD в settings.py DATABASES (Не используется с SQLite).
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres1
```
Можно сменить на нового, прежде создав его и дав все разрешения
для работы с БД (контейнер запущен).
Далее меняем в .env файле.
```
docker-compose exec db psql -U postgres
CREATE USER <username> WITH ENCRYPTED PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <username>; 
```
Указываем какой хост и порт будут использоваться для связи с БД.
HOST и PORT в settings.py DATABASES(Не используется с SQLite).
Имя хоста в нашем случае совпадает с названием контейнера с БД.
```
DB_HOST=db
DB_PORT=5432
```

Запускаем производим развертывание инфраструктуры.

```
docker-compose -f docker-compose-local.yml up -d
```

Применяем миграции, создаем суперюзера и собираем статику в контейнере backend.

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
```

Наполняем БД ингредиентами и тегами.

```
docker-compose exec backend python manage.py loaddatatodb
```

После тестирования останавливаем контейнеры.

```
docker-compose down -v
```

## Инструкция для CI/CD находится в файле foodgram_workflow.yml.

При пуше в ветку master последовательно запускаются четыре задачи (jobs):

- Tests - тестирование проекта на соответствие PEP8. Задействуем модуль actions/setup-python@v2 для запуска пакетов python. 
- Build_and_push_to_docker_hub - создается образ докер контейнера и отправляется в репозиторий докерхаба. Задействуем модуль docker/setup-buildx-action@v1 для сборки Docker образов, docker/login-action@v1 для установки соединения с DockerHub, docker/build-push-action@v2 для отправки собранного образа в репозиторий DockerHub.
- Deploy - развертывание проекта на боевом сервере Яндекс.Облака. Задействуем модуль appleboy/ssh-action@master для инициализации подключения по SSH и выполнения скрипта.
- Send_message - отправка сообщения в тг об успешном выполнении workflow. Задействуем модуль appleboy/telegram-action@master.

Перед первым деплоем необходимо закинуть на сервер два файла: docker-compose.yml и nginx.conf. Команда относительно нахождения в корневой директории проекта.

```
scp /infra/doker-compose.yml /infra/nginx.conf имя_пользователя@адрес_сервера:/home/имя_пользователя/
```

После первого успешного деплоя необходимо на сервере выполнить следующие действия:
- Применяем миграции, создаем суперюзера и собираем статику в контейнере backend.

```
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input 
```

- Наполняем БД ингредиентами и тегами.

```
sudo docker-compose exec backend python manage.py loaddatatodb
```

Для успешного выполнения foodgram_workflow.yml необходимо в настройках репозитория настроить следующие секретные ключи:

- DOCKER_USERNAME и DOCKER_PASSWORD - имя пользователя и пароль от докерхаба.
- HOST, USER, SSH_KEY и PASSPHRASE - ip сервера, имя пользователя на сервере, приватный SSH ключ комьютера, имеющего доступ к боевому серверу, и PASSPHRASE от секретного ключа. 
```
cat ~/.ssh/id_rsa
```
- SECRET_KEY, DEBAG, ALLOWED_HOSTS - секретный ключ Джанги, переменная режима работы сервера, разрешенные хосты для подключения.
- DB_ENGINE, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT - движок, название, пользователь, пароль, хост и порт для работы с БД.


## Примеры работы

Подробная документация доступна по эндпоинту /api/docs/
Для неавторизованных пользователей работа на сайте доступна только в режиме чтения.

## Пользовательские роли

Аноним — может просматривать список пользователей, список ингредиентов, тегов и рецептов.
Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать рецепты, подписываться на рецепты и авторов, добавлять рецепты в список покупок и скачивать список покупок с необходимыми ингредиентами для приготовления рецепта из списка покупок. Может редактировать и удалять свои отзывы. Эта роль присваивается по умолчанию каждому новому пользователю.
Администратор (admin) — полные права на управление всем контентом проекта. Может создавать, редактировать и удалять теги и ингредиенты. Может назначать роли пользователям.
Суперюзер Django — обладает правами администратора (admin)

###### Права доступа: Доступно без токена.

- GET /api/tags/ - получение списка всех тегов.
- GET /api/tags/{id}/ - получение конкретного тега.
- GET /api/ingredients/ - получение списка всех ингредиентов.
- GET /api/ingredients/{id}/ - получение конкретного ингредиента.
- GET /api/recipes/ - получение списка всех рецептов.
- GET /api/recipes/{id}/ - получение конкретного рецепта.
- GET /api/users/ - получение списка всех пользователей.
- GET /api/users/{id}/ - получение конкретного пользователя.
- POST /api/users/ - регистрация нового пользователя.
- POST /api/auth/token/login/ - получение токена.

###### Права доступа: Авторизированный пользователь.

- GET /api/users/me/ - получение собственного профиля.
- GET /api/users/subscriptions/ - получение списка авторов в подписке.
- POST /api/users/{id}/subscribe/ - подписаться на пользователя.
- DELETE /api/users/{id}/subscribe/ - отподписаться от пользователя.
- POST /api/users/set_password/ - изменение пароля.
- POST /api/auth/token/logout/- удаление токена.
- POST /api/recipes/ - создание нового рецепта.
- PATCH /api/recipes/{id}/ - обновление рецепта, доступно только автору рецепта и админу.
- DELETE /api/recipes/{id}/ - удаление рецепта, доступно только автору рецепта и админу.
- GET /api/recipes/download_shopping_cart/ - скачивание списка покупок.
- POST /api/recipes/{id}/shopping_cart/ - добавление рецепта в список покупок.
- DELETE /api/recipes/{id}/shopping_cart/ - удаление рецепта из списока покупок.
- POST /api/recipes/{id}/favorite/ - добавление рецепта в список избранного.
- DELETE /api/recipes/{id}/favorite/ - удаление рецепта из списока избранного.

#### Регистрация нового пользователя

```
POST /api/users/
```

Получение токена:

```
POST /api/auth/token/login/
```

### Примеры работы с API для авторизованных пользователей

Добавление тегов и ингредиентов доступно только через админ панель.

Создание нового рецепта:

```
POST /api/recipes/
```

Обновление рецепта, доступно только автору рецепта и админу:

```
PATCH /api/recipes/{id}/
```

Удаление рецепта, доступно только автору рецепта и админу:

```
DELETE /api/recipes/{id}/
```

Скачивание списка покупок:

```
GET /api/recipes/download_shopping_cart/
```

Добавление рецепта в список покупок:

```
POST /api/recipes/{id}/shopping_cart/
```

Удаление рецепта из списока покупок:

```
DELETE /api/recipes/{id}/shopping_cart/
```

Добавление рецепта в список избранного:

```
POST /api/recipes/{id}/favorite/
```

Удаление рецепта из списока избранного:

```
DELETE /api/recipes/{id}/favorite/
```

### Работа с пользователями:

Получение списка всех пользователей.

```
Права доступа: Доступно всем.
GET /api/users/
```

Добавление пользователя:

```
Права доступа: Доступно всем.
Поля email и username должны быть уникальными.
POST /api/users/
```

Получение пользователя по id:

```
Права доступа: Доступно всем.
GET /api/users/{id}/
```

Получение данных своей учетной записи:

```
Права доступа: Любой авторизованный пользователь
GET /api/users/me/
```

Получение списка авторов в подписке:

```
Права доступа: Любой авторизованный пользователь
GET /api/users/subscriptions/
```

Подписаться на пользователя:

```
Права доступа: Любой авторизованный пользователь
POST /api/users/{id}/subscribe/
```

Отписаться от пользователя:

```
Права доступа: Любой авторизованный пользователь
DELETE /api/users/{id}/subscribe/
```

Изменение пароля:

```
Права доступа: Любой авторизованный пользователь
POST /api/users/set_password/ - изменение пароля.
```

Удаление токена:

```
Права доступа: Любой авторизованный пользователь
POST /api/auth/token/logout/- удаление токена.
```


#### Лицензия
###### Free Software, as Is 
###### _License Free_
###### Authors: [Вячеслав Клепалов](https://github.com/KlepalovS), [Yandex practikum](https://practicum.yandex.ru)
###### 2023
