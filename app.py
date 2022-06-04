import os

from flask import Flask, request, abort

from classes.filehandler import FileHandler
from classes.query import Query
from utils import *

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query/")
def perform_query():

    # Получаем данные из запроса
    cmd1 = request.args.get('cmd1')
    value1 = request.args.get('value1')
    cmd2 = request.args.get('cmd2')
    value2 = request.args.get('value2')
    file_name = request.args.get('file_name')

    # Блок проверок имени файла и самого файла
    if not file_name:
        return abort(400)
    filehandler = FileHandler(file_name=file_name, file_path=DATA_DIR)

    if not filehandler.is_file_exist():
        return abort(400)

    # Получаем данные из файла
    data = filehandler.get_data()

    # Блок проверок команд и выполнения запросов
    if not cmd1 and not cmd2:
        return abort(400)

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
        try:
            query = Query(cmd1, value1)
            result = list(query.execute_query(data))
            result = [row+'\n' for row in result]
            return app.response_class(f'{"".join(result)}', content_type="text/plain")
        except IndexError:
            return {"error": "Incorrect index in value"}

    # Выполняем проверку задан ли только cmd2
    elif not cmd1:
        try:
            if not query_validation(cmd2, value2):
                return abort(400)
        except CommandQueryError as error:
            print(f'Ошибка в запросе cmd2\n {error}')
            return abort(400), 'Упс'
        try:
            query = Query(cmd2, value2)
            result = list(query.execute_query(data))
            result = [row + '\n' for row in result]
            return app.response_class(f'{"".join(result)}', content_type="text/plain")
        except IndexError:
            return {"error": "Incorrect index in value"}

    # Если заданы оба параметра, то выполняется цепочка запросов
    else:

        try:
            if not (query_validation(cmd1, value1) or query_validation(cmd2, value2)):
                return abort(400)
        except CommandQueryError as error:
            print(f'Ошибка в запросе cmd\n {error}')
            return abort(400), 'Упс'

        try:
            query1 = Query(cmd1, value1)
            query2 = Query(cmd2, value2)
            result = query1.execute_query(data)
            result = list(query2.execute_query(result))
            result = [row+'\n' for row in result]
            return app.response_class(f'{"".join(result)}', content_type="text/plain")
        except IndexError:
            return {"error": "Incorrect index in value"}


if __name__ == '__main__':
    app.run()