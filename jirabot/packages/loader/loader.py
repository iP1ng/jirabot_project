"""
Загрузка данных из конфигурационных файлов для многопоточного выполнения
"""


from packages.jira import JiraConnect
from packages.jira import JiraTasks
from packages.postgresql import PostgreSQLDB
from packages.cmd import CMD



from multiprocessing import Pool
import signal



class Workers:
    """
    Методы класса извлекают информацию из конфигурационных файлов и запускают по одному процессу на каждый шаблон задачи
    """

    def __init__(self):
        self.jira_credentials, self.db_credentials, self.task_conf = CMD.get_args()


    def run_worker(self, task_name):
        """
        Метод, отвечающий за считывание конфигурационных файлов и запуск воркера

        :param task_name: Шаблон задачи
        :return:
        """
        DBConnection = PostgreSQLDB(self.db_credentials[self.task_conf[task_name]["database"]]["dbname"],
                                    self.db_credentials[self.task_conf[task_name]["database"]]["dbuser"],
                                    self.db_credentials[self.task_conf[task_name]["database"]]["dbhost"],
                                    self.db_credentials[self.task_conf[task_name]["database"]]["dbport"],
                                    self.db_credentials[self.task_conf[task_name]["database"]]["dbpassword"])

        JiraConnection = JiraConnect.connect_jira(self.jira_credentials[self.task_conf[task_name]["jira"]]["jira_server"],
                                                  self.jira_credentials[self.task_conf[task_name]["jira"]]["jira_user"],
                                                  self.jira_credentials[self.task_conf[task_name]["jira"]]["jira_password"],
                                                  self.jira_credentials[self.task_conf[task_name]["jira"]]["jira_certificate"])

        TaskInstance = JiraTasks(JiraConnection, DBConnection, self.task_conf[task_name])

        TaskInstance.do_task()

        return None


    def run_workers(self):
        """
        Метод, отвечающий за запуск и остановку воркеров

        :return: None
        """
        signal.signal(signal.SIGINT, CMD.signal_handler)

        task_list = list(self.task_conf.keys())
        procs = Pool(len(task_list))
        procs.map(self.run_worker, task_list)

        procs.close()
        procs.join()

        return None