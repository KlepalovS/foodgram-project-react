def get_queryset_filter(queryset, user, value, relation):
    """
    Фильтруем заданый queryset по параметрам value
    и анонимности юзера. Если анон - выводим весь queryset.
    Если значение value равно true или 1, то показываем queryset,
    где заданый параметр true, иначе выводим остальные данные.
    """
    if user.is_anonymous:
        return queryset
    if bool(value):
        return queryset.filter(**{relation: user})
    return queryset.exclude(**{relation: user})
