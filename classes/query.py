from typing import Iterable, List, Set, Any
import re


class Query:
    """
    Объект Query:
    Предназначен для работы с объектами запросов пользователя. Обрабатывает запрос на основании запроса
    """

    def __init__(self, cmd: str, value: str):
        self.cmd = cmd
        self.value = value

    def _filter_data(self, iter_object: Iterable[str]) -> Iterable[str]:
        return filter(lambda text_row: self.value in text_row, iter_object)

    def _sort_data(self, iter_object: Iterable[str]) -> Iterable[str]:
        if self.value == 'asc':
            return sorted(iter_object, reverse=False)
        else:
            return sorted(iter_object, reverse=True)

    def _limit_data(self, iter_object: Iterable[str]) -> Iterable[str]:
        result: list[str] = list(iter_object)[:int(self.value)]
        return result

    def _map_data(self, iter_object: Iterable[str]) -> Iterable[str]:
        result: map[str] = map(lambda text_row: text_row.split(' ')[int(self.value)], iter_object)
        return result

    def _regex_data(self, iter_object):
        # Оставил этот кусок, тоже как рабочий вариант.
        # Может при проверке задания классный куратор скажет какой вариант лучше :-)

        # Запоминаем генератор в лист (на этом моменте я понял, что это плохая идея из-за забивания ресурсов)
        # iter_list = list(iter_object)
        # Находим совпадения
        # matches = list(map(lambda x:  re.findall(self.value, x, re.IGNORECASE | re.DOTALL), iter_list))
        # Получаем индексы по совпадениям
        # indices = [matches.index(i) for i in matches if len(i) != 0]
        # Через __getitem__ получаем элементы из списка данных по индексам
        # result = map(iter_list.__getitem__, list(set(indices)))

        result_list: list = []
        for row in iter_object:
            if re.findall(self.value, row, re.IGNORECASE | re.DOTALL):
                result_list.append(row)
        result: set[str] = set(result_list)
        return result

    def execute_query(self, iter_object: Iterable) -> Iterable[str] | List[str] | Set[str]:
        """
        Метод обрабатывает запрос на основании заданной команды.
        :type iter_object: Iterable
        :param iter_object: итерируемый объект
        :return: result: Iterable[str] - итерируем объект
        """
        if self.cmd == 'filter':
            return self._filter_data(iter_object)

        elif self.cmd == 'sort':
            return self._sort_data(iter_object)

        elif self.cmd == 'unique':
            return set(iter_object)

        elif self.cmd == 'limit':
            return self._limit_data(iter_object)

        elif self.cmd == 'map':
            return self._map_data(iter_object)

        elif self.cmd == 'regex':
            return self._regex_data(iter_object)

        else:
            raise ValueError("Значение должно быть filtet/sort/unique/limit/map/regex")
