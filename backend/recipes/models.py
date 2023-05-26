from django.db import models

from core import constants, validators
from users.models import User


class Tag(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        unique=True,
        help_text='Придумай название для тега',
        validators=(
            validators.MinTwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        )
    )
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=constants.MAX_TAG_COLOR_LENGHT,
        help_text='Пропишите цвет в HEX формате',
        validators=(
            validators.MinTagColorLenghtValidator(constants.MIN_HEX_COLOR_LENGHT),
            validators.TagColorRegexValidator(),
        )
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        unique=True,
        help_text='Введите слаг тега',
        validators=(
            validators.MinTwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.TagSlagRegexValidator(),
        )
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """Возвращаем читаемую связку для админки."""
        return f'{self.name} (цвет: {self.color})'


class Ingredient(models.Model):
    """Модель для ингредиента."""

    name = models.CharField(
        verbose_name='Название ингредиента',
        help_text='Напишите название ингредиента',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        validators=(
            validators.MinTwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        ),
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        help_text='Введите единицу измерения',
        validators=(
            validators.MinMeasurementUnitLenghtValidator(
                constants.MIN_MEASUREMENT_UNIT_LENGHT
            ),
            validators.CyrillicCharRegexValidator()
        ),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'name',
                    'measurement_unit',
                ],
                name='unique_name_measurement_unit',
            ),
        )

    def __str__(self):
        """Возвращаем читаемую связку для админки."""
        return (
            f'{self.name}, {self.measurement_unit}.'
        )


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipe_author',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        help_text='Придумайте название рецепта',
        validators=(
            validators.MinTwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        ),
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Опишите рецепт',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        related_name='ingredients_in_recipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        help_text='Выбирете теги для рецепта',
        related_name='recipe_tags',
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Введите время приготовления рецепта',
        validators=(
            validators.MinCookingTimeValueValidator(constants.MIN_COOKING_TIME),
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('pub_date', 'name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """Возвращаем читаемую связку для админки."""
        return f'{self.name}, автор {self.author.username}.'


class RecipeIngredientAmount(models.Model):
    """
    Связанная модель для указания количества
    ингридента в рецепте.
    """

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество',
        validators=(
            validators.MinIngredientAmountValidator(
                constants.MIN_INGREDIENT_AMOUNT
            ),
        )
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'recipe',
                    'ingredient',
                ],
                name='unique_recipe_ingredient',
            ),
        )
        ordering = ('recipe', 'ingredient',)
        verbose_name = 'Кол-во ингредиента в рецепте'

    def __str__(self):
        """Возвращаем читаемую связку для админки."""
        return (
            f'В {self.recipe.name} содержится '
            f'{self.amount}{self.ingredient.measurement_unit}. '
            f'{self.ingredient.name}.'
        )


class FavoriteRecipe(models.Model):
    """Модель добавления рецепта в избранное."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_recipe_user',
        help_text='Пользователь, в чье избранное добавляется рецепт',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранный рецепт',
        on_delete=models.CASCADE,
        related_name='in_favorite',
        help_text='Рецепт, который нужно добавить в избранное'
    )
    add_to_favorite_date = models.DateTimeField(
        verbose_name='Дата добавления в избранное',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('add_to_favorite_date',)
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe',
                ],
                name='unique_fevorite_user_recipe',
            ),
        )

    def __str__(self):
        """Возвращаем читаемую связку для админки."""
        return (
            f'{self.recipe.name} в избранном у {self.user.username}'
        )


class Cart(models.Model):
    """Модель продуктовой корзины."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
        help_text='Пользователь, в чью корзину добавляется рецепт',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в корзине',
        on_delete=models.CASCADE,
        related_name='in_shopping_cart',
        help_text='Рецепт, который нужно добавить в корзину'
    )
    add_to_shopping_cart_date = models.DateTimeField(
        verbose_name='Дата добавления в корзину',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        ordering = ('add_to_shopping_cart_date',)
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe',
                ],
                name='unique_cart_user_recipe',
            ),
        )

    def __str__(self):
        """Возвращаем читаемую связку для админки."""
        return f'{self.recipe.name} в корзине у {self.user.username}'
