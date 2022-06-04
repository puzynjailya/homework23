from classes.query import Query
from exceptions import CommandQueryError


def query_validation(cmd, value):
    """
    Функция валидации запроса
    :param cmd: str - запрос полученный от cmd1 или cmd2
    :param value: str - запрос полученный от value1 или value2
    :return: True или False в зависимости от того, прошла ли валидация или нет
    """
    if cmd == 'filter':
        return isinstance(value, str)

    elif cmd == 'map' or cmd == 'limit':
        try:
            int(value)
            return True
        except (TypeError, ValueError):
            return False

    elif cmd == 'unique':
        result = False if value != '' else True
        return result

    elif cmd == 'sort':
        result = False if value not in ['asc', 'desc'] else True
        return result

    else:
        raise CommandQueryError


