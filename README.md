![example event parameter](https://github.com/zoesoboleva/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)
# API для сервиса YAMDB

YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.


## Используемые технологии

- python
- django
- drf
- posgresql
- docker

## Запуск проекта
1. Установить docker и docker-compose

    Следуйте [официальной инструкции](https://docs.docker.com/engine/install/).

2. Запустить контейнер
    ```
    docker-compose up
    ```
3. Создание суперпользователя Django
    ```
    docker-compose run web python manage.py createsuperuser
    ```
4. Пример инициализации стартовых данных:
    ```
    docker-compose run web python manage.py loaddata fixtures.json
    ```
3. Остановить контейнеры
    ```
    docker-compose down
    ```

### Некоторые примеры запросов к сервису:

POST `api/v1/auth/signup/`: зарегистрироваться как новый пользователь, указав логин и эл.почту
    
    Пример ответа:
    {
    "email": "1@mail.com",
    "username": "artlover"
    }


GET `api/v1/titles/`: получить список всех произведений
    
    Пример ответа:
    {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "category": {
                "name": "music",
                "slug": "01"
            },
            "genre": [
                {
                    "name": "rock",
                    "slug": "02"
                }
            ],
            "name": "Toxicity",
            "rating": null,
            "year": 17,
            "description": "1s"
    }

GET `api/v1/titles/{title_id}/reviews/`: получить список всех отзывов
    
    Пример ответа:
    {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "text": "Nice",
            "author": "lover",
            "score": 7,
            "pub_date": "2022-11-12T09:47:25.698649Z"
         }
     ]
    }

## Автор
Зоя Соболева
