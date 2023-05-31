# Generated by Django 3.2 on 2023-05-30 18:52

from django.db import migrations, models

import core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(help_text='Опишите рецепт', validators=[core.validators.MinTwoCharValidator(2), core.validators.CyrillicCharRegexValidator()], verbose_name='Описание'),
        ),
    ]