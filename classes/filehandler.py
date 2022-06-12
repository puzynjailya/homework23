import os
from typing import Iterable


class FileHandler:
    """
    Класс FileHandler предназначен для работы с объектами файлами.
    Класс может проверить на наличие файла в заданной директории, создать путь к файлу и получить данные из него в виде
    генератора
    """
    def __init__(self, file_name: str, file_path: str):
        self.file_name = file_name
        self.file_path = file_path

    def is_file_exist(self) -> bool:
        return self.file_name in os.listdir(self.file_path)

    def _create_file_path(self) -> str:
        return os.path.join(self.file_path, self.file_name)

    def get_data(self) -> Iterable[str]:
        with open(self._create_file_path()) as f:
            while True:
                try:
                    row = next(f)
                    yield row
                except StopIteration:
                    break
