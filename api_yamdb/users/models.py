from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
    username = models.CharField(
        verbose_name='Ник пользователя',
        max_length=150,
        null=False,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150,
        null=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=150,
        null=False,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Статус на сайте',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=10,
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
