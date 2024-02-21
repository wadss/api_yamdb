# API YaMDb 
API для проекта YaMDb который собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. 

## Содержание 
- [Технологии](#технологии) 
- [Начало работы](#начало-работы) 
- [To do](#to-do) 
- [Команда проекта](#команда-проекта) 

 

## Технологии 
- [Python 3.9.10]([https://www.gatsbyjs.com/](https://www.python.org/downloads/release/python-3910/)) 
- [Django REST Framework 3.12.4]([https://www.typescriptlang.org/](https://www.django-rest-framework.org/community/release-notes/#3124)) 
- [Django 3.2]([[https://www.typescriptlang.org/](https://www.django-rest-framework.org/community/release-notes/#3124)](https://docs.djangoproject.com/en/5.0/releases/3.2/)) 

 
## Начало работы 
Скачайте репозиторий проекта и перейдите в папку с проектом. 

Разверните виртуальное окружение: 
```sh 
$ py -m venv venv 
``` 
Активируйте виртуальное окружение: 
```sh 
source venv/Scpirts/activate 
``` 
 

## Разработка 

### Требования 
Для установки и запуска проекта, необходим [Python 3.9.10]([https://www.gatsbyjs.com/](https://www.python.org/downloads/release/python-3910/)) 


### Установка зависимостей 
Для установки зависимостей, выполните команду: 
```sh 
pip install -r requirements.txt 
``` 

### Создание и выполнение миграций 
Для создания и выполения миграций, выполните команду: 
```sh 
py manage.py makemigrations 
>>> 
py manage.py migrate 
```

### Наполние БД данными: 
Для того чтоб наполнить БД данными необходимо установить утилиту csvkit выполнил команду в терминале: 
```sh 
pip install csvkit 
``` 

Далее указать файл .csv и название БД в которую будем импортировать данные, например: 
```sh 
csvsql -i sqlite data.csv 
``` 

### Примеры запросов к API 
- http://127.0.0.1:8000/api/v1/auth/token/ - URL получения токена JWT. 
- http://127.0.0.1:8000/api/v1/auth/token/ - URL авторизации. 
- http://127.0.0.1:8000/api/v1/title/ - URL получения списка произведений. 


### Запуск Development сервера 
Чтобы запустить сервер для разработки, выполните команду в папке api_yamdb/api_yamdb: 
```sh 
py manage.py runserver 
``` 

После запуска локального серврера по адресу ниже доступна ReDOC документация с примерами запросов и возвращаемыми данными. 
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