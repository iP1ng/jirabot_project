"""
Взаимодействие с ботом из командной строки
"""


from packages.conf import Task


import os
import sys



class CMD:
    """
    Методы вызова приложения из командной строки
    """

    @staticmethod
    def get_args():
        # You could give all 3 config files
        if len(sys.argv) == 4:
            jira_conf_path = sys.argv[1]
            db_conf_path = sys.argv[2]
            task_conf_path = sys.argv[3]
            # parse configuration
            jira_credentials = Task.load_config(os.path.abspath(jira_conf_path))
            db_credentials = Task.load_config(os.path.abspath(db_conf_path))
            task = Task.load_config(os.path.abspath(task_conf_path))
        # Or just Task config
        elif len(sys.argv) == 2:
            task_conf_path = sys.argv[1]
            # parse configuration
            jira_credentials = Task.load_config(os.path.relpath("configs/jira_configjson"))
            db_credentials = Task.load_config(os.path.relpath("configs/database_config.json"))
            task = Task.load_config(os.path.abspath(task_conf_path))
        # Or use defaults
        else:
            # parse configuration
            jira_credentials = Task.load_config(os.path.relpath("configs/jira_config.json"))
            db_credentials = Task.load_config(os.path.relpath("configs/database_config.json"))
            task = Task.load_config(os.path.relpath("tasks/inn_by_ogrn/inn_by_ogrn.json"))
        return jira_credentials, db_credentials, task

    @staticmethod
    def signal_handler(signal, frame):
        print('Wooops, you killed Jirabot :(')
        sys.exit(0)
