from django.contrib.auth.models import AbstractUser
from django.db import models

from core import constants, validators


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=constants.MAX_EMAEL_LENGHT,
        unique=True,
        help_text='Введите действующий email!',
    )
    username = models.CharField(
        verbose_name='Юзернейм',
        max_length=constants.MAX_NAME_USERNAME_PASSWORD_LENGHT,
        unique=True,
        help_text='Придумате юзернейм!',
        validators=(
            validators.not_me_username_validator,
            validators.LatinCharRegexValidator(),
            validators.MinTwoCharValidator(constants.MIN_TEXT_LENGHT),
        )
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=constants.MAX_NAME_USERNAME_PASSWORD_LENGHT,
        help_text='Введите ваше имя!',
        validators=(
            validators.MinTwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        )
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=constants.MAX_NAME_USERNAME_PASSWORD_LENGHT,
        help_text='Введите вашу фамилию',
        validators=(
            validators.MinTwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        )
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=constants.MAX_NAME_USERNAME_PASSWORD_LENGHT,
        help_text='Введите пароль!'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'username',
                    'email',
                ],
                name='unique_username_email',
            ),
        )

    def __str__(self):
        """Возвращаем читаемую связку в админке."""
        return self.username


class Subscription(models.Model):
    """
    Модель для осуществления подписки
    одного пользователя на другого.
    """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='subscriber_user',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор в подписке',
        related_name='author_in_subscription',
        on_delete=models.CASCADE,
    )
    subscription_date = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now=True,
    )

    class Meta:
        ordering = ('subscription_date',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'user',
                    'author',
                ],
                name='unique_subscription',
            ),
            models.CheckConstraint(
                check=~models.Q(user_id=models.F('author_id')),
                name='no_self_subscription'
            ),
        )

    def __str__(self):
        """Возвращаем читаемую связку Подписки."""
        return (
            f'{self.user} подписан на {self.author}'
        )
