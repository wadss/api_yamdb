from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import validate_username
from api_yamdb.settings import (
    MAX_LENGTH_OF_USERNAME,
    MAX_LENGTH_OF_ROLE,
    MESSAGE_FOR_USERNAME_VALIDATOR,
)


ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    """Модель пользователя."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    username = models.CharField(
        verbose_name='Никнейм пользователя',
        max_length=MAX_LENGTH_OF_USERNAME,
        validators=[
            UnicodeUsernameValidator(
                message=MESSAGE_FOR_USERNAME_VALIDATOR
            ),
            validate_username,
        ],
        unique=True
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES[0][0],
        max_length=MAX_LENGTH_OF_ROLE,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = (
            'username',
            'email',
        )

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
