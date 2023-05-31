from django.core.exceptions import ValidationError
from django.core.validators import (MinLengthValidator, MinValueValidator,
                                    RegexValidator)


class MinTwoCharValidator(MinLengthValidator):
    """Кастомный валидатор на наличие в строке не меньше 2 символов."""

    message = 'Должно быть не меньше 2 символов!'


class MinTagColorLenghtValidator(MinLengthValidator):
    """Кастомный валидатор минимальной длины цвета тега."""

    message = 'Цвет должен состоять минимум из 4 символов!'


class MinMeasurementUnitLenghtValidator(MinLengthValidator):
    """Кастомный валидатор длины названия еддиницы измерения ингредиента."""

    message = 'Единица измерения может состоять минимум из одного символа!'


class MinCookingTimeValueValidator(MinValueValidator):
    """Кастомный валидатор минимального значения времени готовки."""

    message = 'Время готовки должно быть не меньше одной минуты.'


class MinIngredientAmountValidator(MinValueValidator):
    """Кастомный валидатор минимального количества ингредиента."""

    message = 'Количество игредиента не может быть меньше единицы.'


class CyrillicCharRegexValidator(RegexValidator):
    """
    Кастомный валидатор на проверку написания
    текста кириллицей.
    """

    regex = '^[А-Яа-я ,-.]+$'
    message = (
        'Название может быть написано'
        'только кириллицей. Могут использоваться '
        'только буквы и пробелы, тире, запятые, точки.'
    )
    code = 'Invalid char not cirilic'


class TagColorRegexValidator(RegexValidator):
    """
    Кастомный валидатор на верное написание цвета в теге.
    Цвет может быть либо из трех, либо из шести символов
    после знака #.
    """

    regex = '^#[0-9A-Fa-f]{3}$|^#[0-9A-Fa-f]{6}$'
    message = (
        'Цвет должен начинаться с символа # и '
        'может состоять только из цифр 0-9'
        'и латинских букв A-F или a-f. Длина 4 или 7 символов.'
    )
    code = 'Invalid tag HEX color'


class LatinCharRegexValidator(RegexValidator):
    """
    Кастомный валидатор на верное написание латинскими
    буквами с использованием нижнего подчеркивания.
    """

    regex = '^[A-Za-z_]+$'
    message = (
        'Допускается только латиница.'
        'Могут использоваться '
        'только нижние подчеркивания.'
    )
    code = 'Invalid char not latin'


def not_me_username_validator(value):
    """
    Кастомный валидатор, проверяющий, что юзернейм
    не является 'me'.
    """
    if value == 'me':
        raise ValidationError('Юзернейм не может быть me!')
