# Generated by Django 3.2 on 2023-06-04 07:23

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipe_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Введите время приготовления рецепта', validators=[core.validators.MinCookingTimeValueValidator(1)], verbose_name='Время приготовления (в минутах)'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Придумайте название рецепта', max_length=200, validators=[core.validators.MinTwoCharValidator(2), core.validators.CyrillicCharRegexValidator(), core.validators.LatinCharRegexValidator()], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(help_text='Опишите рецепт', validators=[core.validators.MinTwoCharValidator(2)], verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='recipeingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[core.validators.MinIngredientAmountValidator(1)], verbose_name='Количество'),
        ),
    ]