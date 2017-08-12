from src.jira import JiraConnect
from src.jira import JiraTasks
from src.postgresql import PostgreSQLDB
from src.cmd.my_cmd import CMD
from src.logs.my_log import Logs

import threading

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

threads = []

# Handling command line arguments
jira_credentials, db_credentials, task = CMD.get_args()

for task_name in task.keys():
    # Debug
    debug_str = "Starting jirabot instance with \nJIRA params: %s, %s, %s \nDB params: %s, %s, %s, %s, %s" % \
                (jira_credentials[task[task_name]["jira"]]["jira_server"],
                 jira_credentials[task[task_name]["jira"]]["jirauser"],
                 jira_credentials[task[task_name]["jira"]]["jirapassword"],
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
                                              jira_credentials[task[task_name]["jira"]]["jirauser"],
                                              jira_credentials[task[task_name]["jira"]]["jirapassword"])

    TaskInstance = JiraTasks(JiraConnection, DBConnection, task[task_name])

    t = threading.Thread(target=worker)
    threads.append(t)

    # work :)
    t.start()
    print('Now I will work for you :)')


