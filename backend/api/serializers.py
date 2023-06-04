from django.contrib.auth import get_user_model
from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField)
from rest_framework.status import HTTP_400_BAD_REQUEST

from core.constants import MIN_INGREDIENT_AMOUNT
from core.serializers import CustomBaseSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredientAmount, Tag

User = get_user_model()


class RecipMiniFieldseSerializer(CustomBaseSerializer):
    """
    Сериализатор модели рецепта. Содержит меньшее количество
    полей. Нужен для использования в некоторых сериализаторах,
    где не нужны все поля модели.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = ('__all__',)


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомизированный джосеровский сериализатор создания юзера."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    """
    Кастомизированный джосеровский сериализатор отображения юзера.
    Добавили поле статуса подписки на пользователя.
    """

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """
        Определяет статус подписки на пользователя для
        получения значения поля is_subscribed. Если юзер
        анонимный - возвращаем False, иначе проверяем
        наличие есть ли юзер в подписке у автора рецепта.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return (
            user.subscriber_user.filter(author=obj).exists()
        )


class SubscriptionSerializer(CustomUserSerializer):
    """
    Сериализатор для модели подписки юзера на автора рецепта.
    Наследуем его от CustomUserSerializer, чтобы не дублировать
    код. Добавляем два новых поля recipes и recipes_count.
    """

    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'recipes',
        )

    def get_recipes_count(self, obj):
        """Возвращает количество рецептов у автора."""
        return obj.recipe_author.count()

    def get_recipes(self, obj):
        """Возвращаем рецепты у автора в подписке."""
        request = self.context['request']
        recipes_limit = request.GET.get('recipes_limit')
        recipes = obj.recipe_author.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipMiniFieldseSerializer(recipes, many=True, read_only=True).data

    def validate(self, data):
        """
        Проверяем не был ли юзер подписан на автора
        и не осуществляется ли проверка на самого себя.
        """
        author = self.instance
        user = self.context['request'].user
        if user.subscriber_user.filter(author=author).exists():
            raise ValidationError(
                detail='Нельзя дважды подписываться на одного автора!',
                code=HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Подписываться на самого себя запрещено!',
                code=HTTP_400_BAD_REQUEST
            )
        return data


class TagSerializer(ModelSerializer):
    """Сериализатор модели тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('__all__',)


class IngredientSerializer(ModelSerializer):
    """Сериализатор модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('__all__',)


class RecipeIngredientAmountSerializer(ModelSerializer):
    """Сериализатор количества игредиента в рецепте."""

    id = IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredientAmount
        fields = (
            'id',
            'amount',
        )


class ReadRecipeSerializer(CustomBaseSerializer):
    """Сериализатор для вывода рецепта."""

    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    ingredients = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """
        Определяет статус наличия рецпта в избранном у юзера
        для получения значения поля is_favorite. Если юзер
        анонимный - возвращаем False, иначе проверяем
        наличие рецепта у юзера в избранном.
        """
        return (
            self.has_user_related_obj_exists_or_false(
                'favorite_recipe_user', 'recipe', obj
            )
        )

    def get_is_in_shopping_cart(self, obj):
        """
        Определяет статус наличия рецепта в корзине у юзера
        для получения значения поля is_in_shopping_cart.
        Если юзер анонимный - возвращаем False, иначе проверяем
        наличие рецепта у юзера в корзине покупок.
        """
        return (
            self.has_user_related_obj_exists_or_false(
                'shopping_cart_user', 'recipe', obj
            )
        )

    def get_ingredients(self, obj):
        """Получаем игредиенты для вывода в рецепте."""
        return (
            obj.ingredients.values(
                'id',
                'name',
                'measurement_unit',
                amount=F('recipeingredientamount__amount')
            )
        )


class WriteRecipeSerializer(CustomBaseSerializer):
    """Сериализатор для создания нового рецепта."""

    ingredients = RecipeIngredientAmountSerializer(many=True)
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, value):
        """Проверяем правильность выбранных ингредиентов."""
        ingredients = self.get_field_and_no_field_value_validate(
            field='ingredients', value=value
        )
        ingredients_in_recipe = []
        for ingredient in ingredients:
            if ingredient in ingredients_in_recipe:
                raise ValidationError({
                    "ingredients": "Нельзя дважды добавлять ингредиент!"
                })
            if int(ingredient['amount']) < MIN_INGREDIENT_AMOUNT:
                raise ValidationError({
                    "amount": "Количесво ингредиента не может быть меньше 1!"
                })
            ingredients_in_recipe.append(ingredient)
        return value

    def validate_tags(self, value):
        """Проверяем правильность выбранных тегов."""
        tags = self.get_field_and_no_field_value_validate(
            field='tags', value=value
        )
        tags_in_recipe = []
        for tag in tags:
            if tag in tags_in_recipe:
                raise ValidationError({
                    "tags": "Этот тег уже выбран!"
                })
            tags_in_recipe.append(tag)
        return value

    def create(self, validated_data):
        """Создаем новый рецепт."""
        tags, ingredients = self.get_tags_and_ingredients_from_validated_data(
            data=validated_data
        )
        recipe = Recipe.objects.create(**validated_data)
        self.add_tags_and_ingredients_to_recipe(
            recipe=recipe, tags=tags, ingredients=ingredients
        )
        return recipe

    def update(self, instance, validated_data):
        """Обновляем выбранный рецепт."""
        if 'tags' in validated_data:
            instance.tags.clear()
            instance.tags.set(validated_data.pop('tags'))
        if 'ingredients' in validated_data:
            instance.recipeingredientamount_set.all().delete()
            self.create_recipe_ingredients_amount(
                recipe=instance,
                ingredients=validated_data.pop('ingredients')
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Меняем данные для правильного отображения
        после создания/обновления рецепта.
        """
        request = self.context['request']
        context = {'request': request}
        return ReadRecipeSerializer(
            instance=instance,
            context=context,
        ).data
