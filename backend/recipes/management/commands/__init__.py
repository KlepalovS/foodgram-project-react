from .loaddatatodb import LoadIngredientsToDb, LoadTagsToDb

load_ingredients = LoadIngredientsToDb()
load_tags = LoadTagsToDb()

commands = {
    "loadingredientstodb": load_ingredients,
    "loadtagstodb": load_tags,
}
