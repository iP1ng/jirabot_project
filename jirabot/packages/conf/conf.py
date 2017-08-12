"""
Работа с конфигурационными файлами
"""


import json
import os




class Task:
    """
    Шаблон задачи
    Для каждой задачи следует указать параметры подключения к БД,
    параметры подключения к jira,
    параметры задачи
    """

    @staticmethod
    def load_config(config_file):
        with open(config_file, encoding="utf8") as myfile:
            string_myfile = myfile.read().replace('\n', ' ').replace('\r', ' ')
        config = json.loads(string_myfile)
        return config
