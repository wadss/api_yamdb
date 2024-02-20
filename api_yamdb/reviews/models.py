from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import (
    MAX_LENGTH_OF_NAME,
    MAX_LENGTH_OF_SLUG,
    MIN_VALUE_OF_SCORE,
    MAX_VALUE_OF_SCORE,
    MESSAGE_FOR_MIN_SCORE,
    MESSAGE_FOR_MAX_SCORE,
)
from users.models import User
from .validators import validate_year


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        verbose_name='Название категории',
        max_length=MAX_LENGTH_OF_NAME,
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        max_length=MAX_LENGTH_OF_SLUG,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(
        verbose_name='Название жанра',
        max_length=MAX_LENGTH_OF_NAME,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        max_length=MAX_LENGTH_OF_SLUG,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        verbose_name='Название произведения',
        max_length=MAX_LENGTH_OF_NAME,
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска произведения',
        validators=(validate_year,),
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связи жанров и произведений."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = "Произведение - Жанр"
        verbose_name_plural = "Произведения - Жанры"
        ordering = ('title',)

    def __str__(self):
        return f'{self.genre} - {self.title}'


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveIntegerField(
        verbose_name='Оценка на произведение',
        default=0,
        validators=(
            MinValueValidator(
                MIN_VALUE_OF_SCORE,
                message=MESSAGE_FOR_MIN_SCORE,
            ),
            MaxValueValidator(
                MAX_VALUE_OF_SCORE,
                message=MESSAGE_FOR_MAX_SCORE,
            ),
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            )
        ]

    def __str__(self):
        return (f'Отзыв на {self.title} '
        f'от автора {self.author}')


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
