import os

from flask import Flask, request, abort

from classes.filehandler import FileHandler
from classes.query import Query
from utils import *
from typing import List, Iterable

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query/", methods=['POST'])
def perform_query():

    # Получаем данные из запроса
    cmd1: str = request.args.get('cmd1')
    value1: str = request.args.get('value1')
    cmd2: str = request.args.get('cmd2')
    value2: str = request.args.get('value2')
    file_name: str = request.args.get('file_name')

    # Проверка запроса
    if not file_name:
        return abort(400)

    filehandler: FileHandler = FileHandler(file_name=file_name, file_path=DATA_DIR)

    if not filehandler.is_file_exist():
        return abort(400)

    # Получаем данные из файла
    data: Iterable[str] = filehandler.get_data()

    # Выполняем проверку задан ли только cmd1
    if not cmd2:
        try:
            # Проводится валидация запроса
            if not query_validation(cmd1, value1):
                return abort(400)
        except CommandQueryError as error:
            print(f'Ошибка в запросе cmd1\n {error}')
            return abort(400), 'Упс'

        # Выполнение запроса путем цепочки запросов
        result = run_single_param(cmd1, value1, data)
        return app.response_class(f'{"".join(result)}', content_type="text/plain")

    # Выполняем проверку задан ли только cmd2
    elif not cmd1:
        try:
            if not query_validation(cmd2, value2):
                return abort(400)
        except CommandQueryError as error:
            print(f'Ошибка в запросе cmd2\n {error}')
            return abort(400), 'Упс'

        result = run_single_param(cmd2, value2, data)
        return app.response_class(f'{"".join(result)}', content_type="text/plain")

    # Если заданы оба параметра, то выполняется цепочка запросов
    elif cmd1 and cmd2:
        try:
            if not (query_validation(cmd1, value1) or query_validation(cmd2, value2)):
                return abort(400)
        except CommandQueryError as error:
            print(f'Ошибка в запросе cmd\n {error}')
            return abort(400), 'Упс'

        result = run_double_param(cmd1, value1, cmd2, value2, data)
        return app.response_class(f'{"".join(result)}', content_type="text/plain")

    else:
        abort(404)


if __name__ == '__main__':
    app.run()