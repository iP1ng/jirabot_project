"""
Взаимодействие с Jira
"""


from jira import JIRA
from jira.exceptions import JIRAError


import time
import os
import sys
import logging




class JiraConnect:
    """
    Класс содержит метод подключения к серверу JiraConnect
    """

    @staticmethod
    def connect_jira(jira_server, jira_user, jira_password, jira_crt):
        """
        Метод подключения к сервису Jira через basic auth

        :param jira_server: адрес сервера Jira
        :param jira_user: логин пользователя в Jira
        :param jira_password: пароль пользователя в Jira
        :return: Возвращает объект подключения к Jira
        """
        try:
            # Для подключения без верификации сертификата раскомментировать эту строку
            # jira_options = {'server': jira_server, 'verify': False}

            cert_path = os.path.relpath(jira_crt)

            jira_options = {'server': jira_server,
                            'verify': cert_path}
            #jira_options = {'server': jira_server, 'verify': False}
            jira = JIRA(options=jira_options,
                        basic_auth=(jira_user,
                                    jira_password))
            return jira
        except JIRAError as e:
            if e.status_code == 401:
                logging.error('Failed to connect to Jira server: %s' % (e,))
                print('Failed to connect to Jira server: %s' % (e,))
                sys.exit()





class JiraTasks:
    """
    Класс содержит методы для работы с задачами в Jira
    """

    def __init__(self, jiraconnection, dbconnection, task):
        """
        Конструктор класса

        :param jiraconnection: Объект подключения к серверу Jira
        :param dbconnection: Объект подключения к серверу БД
        :param task: Шаблон задачи в Jira
        """
        self.myjira = jiraconnection
        self.dbconnection = dbconnection
        self.task = task


    def list_issues(self, srch_filter):
        """
        Метод для получения списка задач по заданному фильтру

        :param srch_filter: фильтр поиска задач
        :return: возвращает список найденных задач
        """
        issues = self.myjira.search_issues(srch_filter)
        return issues


    def handle_issue_status(self, issue):
        """
        Метод работы с workflow. Переводит задачу в нужный статус.
        Для helpdesk и промышленной Jira workflow отличается.

        :param issue: Задача в Jira
        :return: ничего не возвращает
        """
        if self.task['jira'] == 'helpdesk':
            # 11 и 91 - 'В работе'
            # 21 - 'Выполнено'
            tr = str(self.myjira.find_transitionid_by_name(issue, 'В работе'))
            if tr == '11':
                self.myjira.transition_issue(issue, '11')
                self.myjira.transition_issue(issue, '21')
            elif tr == '91':
                self.myjira.transition_issue(issue, '91')
                self.myjira.transition_issue(issue, '21')
            else:
                self.myjira.transition_issue(issue, '21')
        else:
            # transition to "Resolved" and assign to reporter
            allfields = self.myjira.fields()
            for field in allfields:
                if field['name'] == 'Reporter':
                    fieldid = field['id']
                    reporter = issue.raw['fields'][fieldid]['name']
            # Get all avaliable transitions like id 5 is Resolved
            # https://jira.lanit.ru/rest/api/2/project/HCSINT/statuses
            # TODO make it automatic with find_transitionid_by_name function
            self.myjira.transition_issue(issue, '5', assignee={'name': reporter})


    def get_customfield(self):
        """
        Метод сопоставления названий кастомных полей их идентификаторам.

        :return: Возвращает id кастомного поля, соответствующий кастомному полю из шаблона задачи
        """
        allfields = self.myjira.fields()
        for field in allfields:
            if field['name'] == self.task['field']:
                return field['id']


    def do_task(self):
        """
        Метод выполнения задачи из шаблона с заданными интервалами по времени

        :return: ничего не возвращает
        """

        print("Jirabot ready to work! Searching for tasks with condition %s" % self.task['condition'])
        while True:
            issues = self.myjira.search_issues(self.task['condition'])
            fieldid = self.get_customfield()

            for issue in issues:
                field_value = ((issue.raw['fields'][fieldid].replace(' ', '').replace('\n', '').replace('\r', '')),)
                query_result = self.dbconnection.get_from_db(self.task['query'], field_value)

                jira_comment = ''
                for i in range(len(query_result)):
                    jira_comment = jira_comment + ', '.join(map(str, query_result[i])) + '\n'
                self.myjira.add_comment(issue, jira_comment)

                self.handle_issue_status(issue)

            time.sleep(self.task['periodicity'])
