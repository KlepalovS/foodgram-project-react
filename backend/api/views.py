from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import FoodgramPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             ReadRecipeSerializer, TagSerializer,
                             WriteRecipeSerializer)
from core.constants import ARGUMENTS_TO_ACTION_DECORATORS
from core.servises import (create_and_download_shopping_cart,
                           creating_subscription_between_user_and_author,
                           creation_favorite_or_shopping_cart_recipe,
                           delete_recipe_from_favorite_or_shopping_cart,
                           delete_subscription_between_user_and_author,
                           get_filtered_subscription_queryset,
                           get_subscriptions_serializer_with_pages)
from recipes.models import Cart, FavoriteRecipe, Ingredient, Recipe, Tag

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    Вьюсет для работы с пользователем.
    Наследуем от базового джосеровского UserViewSet.
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = FoodgramPagination

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('post_del'))
    def subscribe(self, request, id):
        """
        Веб-сервис для осуществления подписки и отписки юзера на автора.
        Работает с методами POST и DELETE. Доступен только авторизированным
        пользователям.
        """
        if request.method == 'POST':
            return creating_subscription_between_user_and_author(
                request=request, user=request.user, author_id=id,
            )
        return delete_subscription_between_user_and_author(
            user=request.user, author_id=id
        )

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('get'))
    def subscriptions(self, request):
        """
        Веб-сервис отображающий всех авторов в подписке пользователя.
        Доступно только авторизированному пользователю. Подписки выводятся
        согласно заданной пагинации.
        """
        return (
            self.get_paginated_response(
                get_subscriptions_serializer_with_pages(
                    request=request,
                    pages=self.paginate_queryset(
                        get_filtered_subscription_queryset(user=request.user)
                    )
                ).data
            )
        )


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = FoodgramPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    """Вьюсет для модели рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = FoodgramPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        """Переопределяем метод создания. Добавляем автора."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Назначаем сериализаторы под методы запроса."""
        if self.request.method in SAFE_METHODS:
            return ReadRecipeSerializer
        return WriteRecipeSerializer

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('post_del'))
    def favorite(self, request, pk):
        """
        Веб-сервис для добавления/удаления рецепта
        в/из избранное/избранного. Доступно только
        авторизированному пользователю.
        """
        if request.method == 'POST':
            return creation_favorite_or_shopping_cart_recipe(
                model=FavoriteRecipe, user=request.user, id=pk
            )
        return delete_recipe_from_favorite_or_shopping_cart(
            model=FavoriteRecipe, user=request.user, id=pk
        )

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('post_del'))
    def shopping_cart(self, request, pk):
        """
        Веб-сервис для добавления/удаления рецепта
        в/из список/списка покупок. Доступно только
        авторизированному пользователю.
        """
        if request.method == 'POST':
            return creation_favorite_or_shopping_cart_recipe(
                model=Cart, user=request.user, id=pk
            )
        return delete_recipe_from_favorite_or_shopping_cart(
            model=Cart, user=request.user, id=pk
        )

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('get'))
    def download_shopping_cart(self, request):
        """
        Веб-сервис для скачивания списка покупок.
        Доступно только авторизированному пользователю.
        """
        return create_and_download_shopping_cart(request.user)
