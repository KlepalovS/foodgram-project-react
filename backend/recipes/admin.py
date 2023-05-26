from django.contrib import admin

from recipes.models import (Cart, FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredientAmount, Tag)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Настройка админки для корзины покупок."""

    list_display = (
        'user',
        'recipe',
        'add_to_shopping_cart_date',
    )
    list_filter = (
        'user',
        'recipe',
    )


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Настройка админки для избранных рецептов."""

    list_display = (
        'user',
        'recipe',
        'add_to_favorite_date',
    )
    list_filter = (
        'user',
        'recipe',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка админки для модели ингредиентов."""

    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка админки для модели рецептов."""

    list_display = (
        'name',
        'author',
        'in_favorite_count',
    )
    list_filter = (
        'author__username',
        'name',
        'tags',
    )
    readonly_fields = (
        'in_favorite_count',
    )

    def in_favorite_count(self, obj):
        """
        Возвращаем расчет кол-ва добавления
        в избранное рецепта.
        """
        return obj.in_favorite.count()

    in_favorite_count.short_description = 'Добавлений в избранное'


@admin.register(RecipeIngredientAmount)
class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    """
    Настройка админки для связанной модели
    добавления кол-ва ингредиента в рецепт.
    """

    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка админки для модели тегов."""

    list_display = (
        'name',
        'slug',
    )
    list_filter = (
        'name',
    )
