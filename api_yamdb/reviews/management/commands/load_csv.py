import csv
import logging

from django.core.management import BaseCommand

from reviews.models import Title, Category, Genre, GenreTitle, Review, Comment
from users.models import User
from api_yamdb.settings import BASE_DIR

FILE_DIRS = 'static/data/'

logger = logging.getLogger(__name__)


def load_category():
    if Category.objects.exists():
        return

    file_path = BASE_DIR / (FILE_DIRS + 'category.csv')
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        categories = []
        for row in data:
            category = Category(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
            categories.append(category)
        if categories:
            Category.objects.bulk_create(categories)


def load_genre():
    if Genre.objects.exists():
        return

    file_path = BASE_DIR / (FILE_DIRS + 'genre.csv')
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        genres = []
        for row in data:
            genre = Genre(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
            genres.append(genre)
        if genres:
            Genre.objects.bulk_create(genres)


def load_title():
    if Title.objects.exists():
        return

    file_path = BASE_DIR / (FILE_DIRS + 'titles.csv')
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        titles = []
        for row in data:
            title = Title(
                id=row[0],
                name=row[1],
                year=row[2],
                category=Category.objects.get(id=row[3])
            )
            titles.append(title)
        if titles:
            Title.objects.bulk_create(titles)


def load_genre_title():
    if GenreTitle.objects.exists():
        return

    file_path = BASE_DIR / (FILE_DIRS + 'genre_title.csv')
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        genres_titles = []
        for row in data:
            genre_title = GenreTitle(
                title=Title.objects.get(id=row[1]),
                genre=Genre.objects.get(id=row[2])
            )
            genres_titles.append(genre_title)
        if genres_titles:
            GenreTitle.objects.bulk_create(genres_titles)


def load_users():
    if User.objects.count() > 1:
        return

    file_path = BASE_DIR / (FILE_DIRS + 'users.csv')
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        users = []
        for row in data:
            user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
            users.append(user)
        if users:
            User.objects.bulk_create(users)


def load_reviews():
    if Review.objects.exists():
        return

    file_path = BASE_DIR / (FILE_DIRS + 'review.csv')
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        reviews = []
        for row in data:
            review = Review(
                id=row[0],
                title_id=Title.objects.get(id=row[1]).id,
                text=row[2],
                author=User.objects.get(id=row[3]),
                score=row[4],
                pub_date=row[5]
            )
            reviews.append(review)
        if reviews:
            Review.objects.bulk_create(reviews)


def load_comments():
    if Comment.objects.exists():
        return

    file_path = BASE_DIR / (FILE_DIRS + 'comments.csv')
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        comments = []
        for row in data:
            comment = Comment(
                id=row[0],
                review_id=Review.objects.get(id=row[1]).id,
                text=row[2],
                author=User.objects.get(id=row[3]),
                pub_date=row[4]
            )
            comments.append(comment)
        if comments:
            Comment.objects.bulk_create(comments)


class Command(BaseCommand):
    help = 'Loads data from csv file to database'

    def handle(self, *args, **options):
        load_category()
        load_genre()
        load_title()
        load_genre_title()
        load_users()
        load_reviews()
        load_comments()
        logger.info('Data loaded successfully')
