from classes.query import Query
from exceptions import CommandQueryError
from typing import Iterable, List, Union


def query_validation(cmd: str, value: str) -> bool:
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

    elif cmd == 'regex':
        result = False if not value else True
        return result

    else:
        raise CommandQueryError


def run_single_param(cmd: str, value: str, datafile: Iterable[str]) -> Union[list | dict]:
    try:
        query: Query = Query(cmd, value)
        result: List[str] = list(query.execute_query(datafile))
        result: list = [row + '\n' for row in result]
        return result

    except IndexError:
        return {"Ошибка": "Проверьте корректность выполняемого запроса"}


def run_double_param(cmd1: str,
                     value1: str,
                     cmd2: str,
                     value2: str,
                     datafile: Iterable[str]) -> Union[list | dict | Iterable[str]]:
    try:
        query1: Query = Query(cmd1, value1)
        query2: Query = Query(cmd2, value2)
        result: Iterable[str] = query1.execute_query(datafile)
        result: List[str] = list(query2.execute_query(result))
        result: list = [row + '\n' for row in result]
        return result

    except IndexError:
        return {"Ошибка": "Проверьте корректность выполняемого запроса"}
