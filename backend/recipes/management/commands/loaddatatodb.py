import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient, Tag


class LoadIngredientsToDb(BaseCommand):
    """
    Команда для загрузки ингредиентов из файла
    ingredients.json в таблицу ингредиентов в
    базе данных.
    """

    help = 'Загружает ингредиенты из ingredients.json в БД'

    def handle(self, *args, **options):
        with open(
            os.path.join(settings.BASE_DIR, 'data', 'ingredients.json')
        ) as file:
            ingredients_data = json.load(file)
            for ingredient_in_data in ingredients_data:
                model = Ingredient()
                model.name = ingredient_in_data['name']
                model.measurement_unit = ingredient_in_data['measurement_unit']
                model.save()
            self.stdout.write('Загрузка данных из ingredients.json завершена!')


class LoadTagsToDb(BaseCommand):
    """
    Команда для загрузки тегов из файла tags.json
    в таблицу ингредиентов в базе данных.
    """

    help = 'Загружает теги из tags.json в БД'

    def handle(self, *args, **options):
        with open(
            os.path.join(settings.BASE_DIR, 'data', 'tags.json')
        ) as file:
            tags_data = json.load(file)
            for tag_in_data in tags_data:
                model = Tag()
                model.name = tag_in_data['name']
                model.color = tag_in_data['color']
                model.slug = tag_in_data['slug']
                model.save()
            self.stdout.write('Загрузка данных из tags.json завершена!')


class Command(BaseCommand):
    """Комманда для загрузки данных в БД."""

    help = 'Загружаем данные из ingredients.json и tags.json в БД'

    def handle(self, *args, **options):
        load_ingredients = LoadIngredientsToDb()
        load_tags = LoadTagsToDb()
        load_ingredients.handle()
        load_tags.handle()
        self.stdout.write('Все данные загружены!')
