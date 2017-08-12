import unittest


from src.jira import JiraConnect
from src.cmd.my_cmd import CMD


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.jira_credentials, self.db_credentials, self.task = CMD.get_args()
        self.standart_jira_task_name = 'test'
        self.helpdesk_jira_task_name = 'test_helpdesk'
        self.JiraConnection = JiraConnect.connect_jira(
                                                    self.jira_credentials[self.task[self.standart_jira_task_name]["jira"]]["jira_server"],
                                                    self.jira_credentials[self.task[self.standart_jira_task_name]["jira"]]["jirauser"],
                                                    self.jira_credentials[self.task[self.standart_jira_task_name]["jira"]]["jirapassword"])
        self.HelpdeskJiraConnection = JiraConnect.connect_jira(
                                                    self.jira_credentials[self.task[self.helpdesk_jira_task_name]["jira"]]["jira_server"],
                                                    self.jira_credentials[self.task[self.helpdesk_jira_task_name]["jira"]]["jirauser"],
                                                    self.jira_credentials[self.task[self.helpdesk_jira_task_name]["jira"]]["jirapassword"])

    def test_standart_jira_connection(self):
        self.assertEqual(self.JiraConnection.current_user(), 'ASoldatov')

    def test_helpdesk_jira_connection(self):
        self.assertEqual(self.HelpdeskJiraConnection.current_user(), 'jirabot')

if __name__ == '__main__':
    unittest.main()