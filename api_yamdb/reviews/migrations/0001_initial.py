# Generated by Django 3.2 on 2024-02-13 03:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL;разрешены символы латиницы,цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL;разрешены символы латиницы,цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название произведения')),
                ('year', models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2024, 'Нельзя добавлять произведения, которые еще не вышли(год выпуска не может быть больше текущего)'), django.core.validators.MinValueValidator(1, 'Год не может быть отрицательным значением')], verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория')),
                ('genres', models.ManyToManyField(related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('name',),
            },
        ),
    ]
