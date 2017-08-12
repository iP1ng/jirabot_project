"""
Jirabot - автоматизация получения данных из PostgreSQL через Jira
"""


from packages.jira import JiraConnect
from packages.jira import JiraTasks
from packages.postgresql import PostgreSQLDB
from packages.cmd import CMD


from logs import Logs


import threading


import signal
import time



def worker():
    """
    Функция-воркер, запускает каждый шаблон задачи в своем треде

    :param task: Шаблон задачи
    :return:
    """
    TaskInstance.do_task()


# Init logging with default params
log = Logs()
log.init_logfile()

signal.signal(signal.SIGINT, CMD.signal_handler)

threads = []

# Handling command line arguments
jira_credentials, db_credentials, task = CMD.get_args()

for task_name in task.keys():

    # Debug
    debug_str = "Starting jirabot instance with \nJIRA params: %s, %s, %s \nDB params: %s, %s, %s, %s, %s" % \
                (jira_credentials[task[task_name]["jira"]]["jira_server"],
                 jira_credentials[task[task_name]["jira"]]["jira_user"],
                 jira_credentials[task[task_name]["jira"]]["jira_password"],
                 db_credentials[task[task_name]["database"]]["dbname"],
                 db_credentials[task[task_name]["database"]]["dbuser"],
                 db_credentials[task[task_name]["database"]]["dbhost"],
                 db_credentials[task[task_name]["database"]]["dbport"],
                 db_credentials[task[task_name]["database"]]["dbpassword"])
    log.debug_log(debug_str)

    # get connections
    DBConnection = PostgreSQLDB(db_credentials[task[task_name]["database"]]["dbname"],
                                db_credentials[task[task_name]["database"]]["dbuser"],
                                db_credentials[task[task_name]["database"]]["dbhost"],
                                db_credentials[task[task_name]["database"]]["dbport"],
                                db_credentials[task[task_name]["database"]]["dbpassword"])

    JiraConnection = JiraConnect.connect_jira(jira_credentials[task[task_name]["jira"]]["jira_server"],
                                              jira_credentials[task[task_name]["jira"]]["jira_user"],
                                              jira_credentials[task[task_name]["jira"]]["jira_password"],
                                              jira_credentials[task[task_name]["jira"]]["jira_certificate"])

    TaskInstance = JiraTasks(JiraConnection, DBConnection, task[task_name])

    t = threading.Thread(target=TaskInstance.do_task)
    threads.append(t)

    # work :)
    t.daemon = True
    t.start()

# keeping main process alive
while True:
    time.sleep(1)



