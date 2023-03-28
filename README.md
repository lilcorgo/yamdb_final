# api_yamdb
Проект _YaMDb_ собирает отзывы пользователей на произведения.

Произведения делятся на категории, такие как `«Книги»`, `«Фильмы»`, `«Музыка»`. 

Благодарные или возмущённые пользователи оставляют к произведениям текстовые 
отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое 
число); из пользовательских оценок формируется усреднённая оценка произведения 
— рейтинг (целое число). На одно произведение пользователь может оставить 
только один отзыв.
Пользователи могут оставлять комментарии к отзывам.

## Технологии

- Python 3.7.14
- Django 2.2.16
- Django REST Framework 3.12.4
- Библиотеки Djoser и Simple JWT

### Запускаем проект:

Клонируем репозиторий:

```
git clone https://github.com/lilcorgo/yamdb_final
```
Переходим в него в командной строке:
```
cd api_yamdb
```

Разворачиваем контейнеры 
```
docker-compose up
```

Выполняем миграции:
```
docker-compose exec python manage.py makemigrations
```
```
docker-compose exec python manage.py migrate
```
Наполняем базу данных из csv файлов:
```
docker-compose exec python manage.py import_csv
```
Собираем статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```

### Статус workflow
![Status of api_yamdb project workflow](https://github.com/Sergey-K2/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

### Документация
```
http://127.0.0.1/redoc/
```

### Пример заполнения .env
```
Какая БД:
DB_ENGINE=django.db.backends.postgresql
Имя БД:
DB_NAME= "your name"
Юзернейм БД
POSTGRES_USER= "your username"
Пароль БД:
POSTGRES_PASSWORD= "your password"
Local host:
DB_HOST=127.0.0.1
Порт БД:
DB_PORT=5432
```

### Проект доступен по адресу
```
http://158.160.34.227/admin/login/?next=/admin/
```