from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from api.serializers import RecipMiniFieldseSerializer, SubscriptionSerializer
from recipes.models import Recipe, RecipeIngredientAmount
from users.models import Subscription

User = get_user_model()


def _get_author(author_id):
    """
    Получает автора по id из запроса.
    Если автор не найден - вызывает ошибку 404.
    """
    return get_object_or_404(User, id=author_id)


def creating_subscription_between_user_and_author(
        request, user, author_id
):
    """
    Осуществляет подписку юзера на автора.
    Возвращает ответ с сериализованными данными
    и статус успешного создания. Если автор не найден,
    то вызывается ошибка 404.
    """
    author = _get_author(author_id)
    serializer = SubscriptionSerializer(
        author,
        data=request.data,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    Subscription.objects.create(user=user, author=author)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_subscription_between_user_and_author(user, author_id):
    """
    Удаляет подписку юзера на конкретного автора.
    Если автор не найден - вызывает ошибку 404.
    Если подписка отсутствует - вызывает ошибку 404.
    """
    subscription = get_object_or_404(
        Subscription,
        user=user,
        author=_get_author(author_id),
    )
    subscription.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def get_filtered_subscription_queryset(user):
    """Получаем queryset авторов на которых подписан юзер."""
    return User.objects.filter(author_in_subscription__user=user)


def get_subscriptions_serializer_with_pages(request, pages):
    """Получаем сериализатор для вывода списка всех подписок у юзера."""
    return SubscriptionSerializer(
        pages,
        many=True,
        context=({"request": request})
    )


def creation_favorite_or_shopping_cart_recipe(model, user, id):
    """
    Добавляет рецепт в избранное или список покупок
    в зависимости от переданной модели. Если рецепт не
    найден - передает ошибку 404. Если рецепт ранее был
    добавлен - передает ошибку 400. При успешном выполнении
    возвращает статус 201 и сериализованные данные.
    """
    recipe = get_object_or_404(Recipe, id=id)
    if model.objects.filter(user=user, recipe=recipe).exists():
        return Response(
            {"errors": "Рецепт уже добавлен!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    model.objects.create(user=user, recipe=recipe)
    serializer = RecipMiniFieldseSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_recipe_from_favorite_or_shopping_cart(model, user, id):
    """
    Удаляет рецепт из избранного или списка покупок
    в зависимости от преданной модели. Если рецепт ранее был
    удален - передает ошибку 400. При успешном выполнении
    возвращает статус 204.
    """
    favorite_or_in_shopping_cart_recipe = model.objects.filter(
        user=user, recipe__id=id
    )
    if favorite_or_in_shopping_cart_recipe.exists():
        favorite_or_in_shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"errors": "Рецепт уже удален!"},
        status=status.HTTP_400_BAD_REQUEST,
    )


def _create_shopping_cart_text(user, ingredients, date):
    """Получаем текст списка покупок."""
    text = (
        f'Привет, {user.first_name}!\n\n'
        f'Вот твой список покупок на {date.strftime("%d.%m")}.\n\n'
        'Для выбранных рецептов нужны игредиенты:\n\n'
    )
    text += '\n'.join([
        f' - {ingredient["ingredient__name"]} '
        f'({ingredient["ingredient__measurement_unit"]})'
        f' - {ingredient["in_shopping_cart_ingredient_amount"]}'
        for ingredient in ingredients
    ])
    text += f'\n\nПолучено с помощью Foodgram {date.strftime("%Y")}.'
    return text


def create_and_download_shopping_cart(user):
    """
    Создает и скачивает список покупок пользователя.
    Производит подсчет необходимых ингредиентов
    в рецептах из списка покупок. Формирует текстовый
    файл и выгружает его.
    """
    ingredients = RecipeIngredientAmount.objects.filter(
        recipe__in_shopping_cart__user=user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(in_shopping_cart_ingredient_amount=Sum('amount'))
    shopping_list_date = timezone.now()
    cart_text = _create_shopping_cart_text(
        user, ingredients, shopping_list_date
    )

    response = HttpResponse(cart_text, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename="foodgram_shopping_cart.txt"'
    )
    return response
