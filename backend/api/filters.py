from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import FilterSet, filters

from core.filters import get_queryset_filter
from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientFilter(FilterSet):
    """
    Кастомный фильтр для ингредиентов.
    Фильтрация производится сначала по точному вхождению начала названия,
    затем по вхождению любой подстроки в названии.

    """

    name = filters.CharFilter(method='ingredient_name_filter')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def ingredient_name_filter(self, queryset, name, value):
        """
        Осуществляет поиск сначала по вхождению в имя ингредиента,
        а затем происходит фильтрация по вхождению в любом месте.
        """
        return queryset.filter(
            Q(name__startswith=value) | Q(name__contains=value)
        )


class RecipeFilter(FilterSet):
    """
    Кастомный фильтр для рецептов.
    Доступна фильтрация по избранному, автору, списку покупок и тегам.
    """

    is_favorited = filters.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def is_favorited_filter(self, queryset, name, value):
        """
        Осуществляем фильтрацию по полю is_favorited.
        Если анон - возвращаем весь queryset без фильтрации.
        Если флаг установлен
        """
        return get_queryset_filter(
            queryset=queryset,
            user=self.request.user,
            value=value,
            relation='in_favorite__user'
        )

    def is_in_shopping_cart_filter(self, queryset, name, value):
        """Осуществляем фильтрацию по полю is_in_shopping_cart_filter."""
        return get_queryset_filter(
            queryset=queryset,
            user=self.request.user,
            value=value,
            relation='in_shopping_cart__user'
        )
