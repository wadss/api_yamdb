from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL;'
            'разрешены символы латиницы,'
            'цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL;'
            'разрешены символы латиницы,'
            'цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        blank=False,
        null=False,
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(
                datetime.now().year,
                'Нельзя добавлять произведения, которые еще не вышли'
                '(год выпуска не может быть больше текущего)'
            ),
            MinValueValidator(
                1,
                'Год не может быть отрицательным значением'
            )
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
