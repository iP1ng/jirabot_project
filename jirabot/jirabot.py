"""
Jirabot - автоматизация получения данных из PostgreSQL через Jira
"""


from logs import Logs


from packages.loader import Workers




log = Logs()
log.init_logfile()

w = Workers()
run = w.run_workers()




