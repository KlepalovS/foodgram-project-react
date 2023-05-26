from rest_framework import serializers

from recipes.models import (Cart, FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredientAmount, Tag)


class  TagSerializer(serializers.Serializer):
    """Сериализатор модели тегов."""

    