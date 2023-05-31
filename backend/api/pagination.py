from rest_framework import pagination


class FoodgramPagination(pagination.PageNumberPagination):
    """
    Собственный пагинатор проекта с возможностью
    у пользователя самостоятельно устанавливать
    количество объектов на странице через параметр
    "limit".
    """

    page_size_query_param = "limit"
