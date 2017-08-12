import logging


class Logs:
    """
    Методы логирования приложения
    """
    def __init__(self, logfile = 'logs/jirabot.log', loglevel = logging.DEBUG, logformat = '%(asctime)s %(message)s'):
        self.logfile = logfile
        self.loglevel = loglevel
        self.logformat = logformat

    def init_logfile(self):
        # appends messages to logfile
        logging.basicConfig(filename=self.logfile, level=self.loglevel, format=self.logformat)

    @staticmethod
    def debug_log(text):
        logging.debug(text)
