from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Subscription

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Кастомизация админки модели пользователя."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'email',
        'username',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Кастомизация админки модели подписки на пользователя.
    """

    list_display = (
        'user',
        'author',
        'subscription_date',
    )
    list_filter = (
        'user',
        'author',
    )
