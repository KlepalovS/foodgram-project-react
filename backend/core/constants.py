from rest_framework.permissions import IsAuthenticated

MAX_EMAEL_LENGHT = 254
MAX_TAG_COLOR_LENGHT = 7
MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT = 200
MAX_NAME_USERNAME_PASSWORD_LENGHT = 150
MIN_TEXT_LENGHT = 2
MIN_HEX_COLOR_LENGHT = 4
MIN_MEASUREMENT_UNIT_LENGHT = 1
MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMOUNT = 1
ARGUMENTS_TO_ACTION_DECORATORS = {
    'post_del': {
        'methods': ('post', 'delete',),
        'detail': True,
        'permission_classes': (IsAuthenticated,),
    },
    'get': {
        'detail': False,
        'permission_classes': (IsAuthenticated,),
    },
}
