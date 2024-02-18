from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    """Проверка на превышение текущего года."""

    current_year = timezone.now().year
    if year > current_year:
        raise ValidationError(
            'Некорректно указан год. '
            f'Значение не может превышать: {current_year}'
        )
