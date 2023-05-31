import base64

from django.core.files.base import ContentFile
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ImageField, ModelSerializer

from recipes.models import Ingredient, RecipeIngredientAmount


class Base64ImageField(ImageField):
    """Кастомное поле для работы с изображениями в формате base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CustomBaseSerializer(ModelSerializer):
    """
    Кастомный сериализатор для добавления сериализаторам
    дополнительных методов воизбежании дублирования кода.
    """

    image = Base64ImageField()

    def get_not_anon_user_from_context_or_none(self):
        """
        Получает юзера из контекста запроса, если он авторизован.
        Иначе возвращает None.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return None
        return user

    def has_user_related_obj_exists_or_false(
            self, related_name: str, field: str, value
    ) -> bool:
        """
        Возвращает проверку наличия у авторизованного юзера
        связанного объекта.
        Передаем строковое значение related_name, название
        проверяемого поля и значение (обьект проверки). На выходе
        получаем булевое значение наличия связи между обьектами,
        если юзер авторизован, иначе получаем False.
        """
        user = self.get_not_anon_user_from_context_or_none()
        if self.get_not_anon_user_from_context_or_none():
            related_manager = getattr(user, related_name)
            return related_manager.filter(**{field: value}).exists()
        return False

    def create_recipe_ingredients_amount(self, recipe, ingredients):
        """Заносим данные в таблицу количества ингредиента в рецепте."""
        RecipeIngredientAmount.objects.bulk_create(
            [RecipeIngredientAmount(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            )for ingredient in ingredients]
        )

    def get_field_and_no_field_value_validate(self, field, value):
        """
        Присваиваем проверяемому полю задаваемое значение
        и проверяем на пустое значение.
        """
        field = value
        if not field:
            raise ValidationError({
                "{field}": "Нельзя ничего не выбрать!"
            })
        return field

    def get_tags_and_ingredients_from_validated_data(self, data):
        """Получаем теги и ингредиенты для дальнейшей работы с ними."""
        tags = data.pop('tags')
        ingredients = data.pop('ingredients')
        return tags, ingredients

    def add_tags_and_ingredients_to_recipe(self, recipe, tags, ingredients):
        """
        Добавляем значение полей тегов и ингредиентов
        к рецепту при создании или изминении рецепта.
        """
        recipe.tags.set(tags)
        self.create_recipe_ingredients_amount(
            recipe=recipe,
            ingredients=ingredients
        )
