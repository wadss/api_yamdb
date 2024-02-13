# Generated by Django 3.2 on 2024-02-13 12:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_rename_genres_title_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2024, 'Нельзя добавлять произведения, которые еще не вышли(год выпуска не может быть больше текущего)'), django.core.validators.MinValueValidator(0, 'Год не может быть отрицательным значением')], verbose_name='Год выпуска'),
        ),
    ]
