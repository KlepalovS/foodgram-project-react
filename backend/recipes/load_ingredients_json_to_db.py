"""
Этот скрипт для загрузки в БД ингредиентов
из файла ingredients.json. Загрузка осуществляется
в таблицу Ingredients. Для выполнения скрипта
необходимо запустить shell терминал Django. Для
этого выполним:
'''
python3 manage.py shell
'''
Затем необходимо в терминале выполнить команду:
'''
exec(open('recipes/load_ingredients_json_to_db.py').read())
'''
После выполнения команды, успешную загрузку
можно проверить открыв админ-панель Django и
посмотреть таблицу Ингредиенты.
"""
import json

from recipes.models import Ingredient

with open('../data/ingredients.json', 'r') as file:
    data = json.load(file)
    for obj in data:
        model = Ingredient()
        model.name = obj['name']
        model.measurement_unit = obj['measurement_unit']
        model.save()
