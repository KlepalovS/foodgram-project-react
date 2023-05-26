from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        help_text='Введите действующий email!',
    )
    username = models.CharField(
        verbose_name='Юзернейм',
        max_length=150,
        unique=True,
        help_text='Придумате юзернейм!',
        validators=(RegexValidator(
            regex='^[A-Za-z.@+-]+$',
            message=(
                'Юзернейм должен содержать только буквы, '
                'цифры, знак подчеркивания, точку, знак плюс, '
                'знак минус и знак @'
            ),
            code='Invalid username',
        ),)
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        help_text='Введите ваше имя!',
        validators=(RegexValidator(
            regex='^[А-Яа-я-]+$',
            message=(
                'Имя должно содержать только буквы, '
                'знак подчеркивания и тире'
            ),
            code='Invalid first_name',
        ),)
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        help_text='Введите вашу фамилию',
        validators=(RegexValidator(
            regex='^[А-Яа-я-]+$',
            message=(
                'Фамилия должна содержать только буквы, '
                'знак подчеркивания и тире'
            ),
            code='Invalid last_name',
        ),)
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        help_text='Придумайте пароль!',
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
        related_name='user_in_subscription',
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
