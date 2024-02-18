# API YaMDb
API для проекта YaMDb который собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-ci/cd)
- [Contributing](#contributing)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии
- [Python 3.9.10]([https://www.gatsbyjs.com/](https://www.python.org/downloads/release/python-3910/))
- [Django REST Framework 3.12.4]([https://www.typescriptlang.org/](https://www.django-rest-framework.org/community/release-notes/#3124))
- [Django 3.2]([[https://www.typescriptlang.org/](https://www.django-rest-framework.org/community/release-notes/#3124)](https://docs.djangoproject.com/en/5.0/releases/3.2/))

## Использование
Скачайте репозиторий проекта и перейди в папку с проектом.

Разверниет виртуальное окружение:
```sh
$ py -m venv venv
```

## Разработка

### Требования
Для установки и запуска проекта, необходим [Python 3.9.10]([https://www.gatsbyjs.com/](https://www.python.org/downloads/release/python-3910/))

### Установка зависимостей
Для установки зависимостей, выполните команду:
```sh
pip install -r requirements.txt
```

### Запуск Development сервера
Чтобы запустить сервер для разработки, выполните команду в папке api_yamdb/api_yamdb:
```sh
py manage.py runserver
```

После запуска локального серврера по адресу ниже доступна ReDOC документация с примерами запросов и возвращаемыми.
http://127.0.0.1:8000/redoc/

### Зачем вы разработали этот проект?
Чтобы был.

## To do
- [x] Добавить крутое README
- [ ] Всё переписать
- [ ] Не писать говнокод на Python;)

## Команда проекта
- [Ярослав Пащенко](https://github.com/wadss) — Team Lead
- [Данияр Альжанов](https://github.com/DaniyarAlzhanov) - Developer
- [Кирилл Петров](https://github.com/KerilPetrov) - Developer
- [Роман Зарубин](https://github.com/Romioyar) - Developer
