class Query:
    """
    Объект Query:
    Предназначен для работы с объектами запросов пользователя. Обрабатывает запрос на основании запроса
    """

    def __init__(self, cmd, value):
        self.cmd = cmd
        self.value = value


    def execute_query(self, iter_object):
        """
        Метод обрабатывает запрос на основании заданной команды.
        :param iter_object: итерируемый объект
        :return: _iter_ - итерируем объект
        """
        if self.cmd == 'filter':
            return filter(lambda row: self.value in row, iter_object)

        if self.cmd == 'sort':
            if self.value == 'asc':
                return sorted(iter_object, reverse=False)
            else:
                return sorted(iter_object, reverse=True)

        if self.cmd == 'unique':
            return set(iter_object)

        if self.cmd == 'limit':
            result = list(iter_object)[:int(self.value)]
            return result

        if self.cmd == 'map':
            result = map(lambda row: row.split(' ')[int(self.value)], iter_object)
            return result










