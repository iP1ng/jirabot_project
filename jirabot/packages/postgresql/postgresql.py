"""
Взаимодействие с PostgreSQL
"""


import psycopg2
import logging
import sys




class PostgreSQLDB:
    """
    Класс содержит методы подключения к БД PostgreSQL и работы с данными в БД PostgreSQL.
    """


    def __init__(self, dbname, username, host, port, password):
        """
        Конструктор класса

        :param dbname: имя базы данных
        :param username: имя пользователя
        :param host: адрес сервера базы данных
        :param port: порт сервера базы данных
        :param password: пароль пользователя
        """
        self.dbname = dbname
        self.username = username
        self.host = host
        self.port = port
        self.password = password


    def connect_db(self):
        """
        Метод подключения к БД PostgreSQL

        :return: при успешном подключении возвращает объекты подключения и курсора
        """
        try:
            conn = psycopg2.connect("dbname=%s "
                                    "user=%s "
                                    "host=%s "
                                    "port=%s "
                                    "password=%s"
                                    % (self.dbname,
                                       self.username,
                                       self.host,
                                       self.port,
                                       self.password))
            cursor = conn.cursor()
            return conn, cursor
        except Exception as e:
            logging.error("Failed to connect to database %s: %s" % (self.dbname, e.message))
            return None


    def get_from_db(self, sql_script, param=None):
        """
        Метод получения данных из БД PostgreSQL.
        При ошибке пытается повторить запрос до 5 раз, иначе выключает приложение.

        :param sql_script: текст выполняемого sql скрипта
        :param param: параметры выполняемого sql скрипта
        :return: при успешном выполнении возвращает полный набор данных из БД PostgreSQL
        """
        retry_number = 5

        for i in range(retry_number):
            try:
                conn, query = self.connect_db()
            except Exception as e:
                logging.warning("Error while connecting to database %s: %s" % (self.dbname, e.message))

            try:
                query.execute(sql_script, param)
                conn.commit()

                result = query.fetchall()

                query.close()
                conn.close()

                return result
            except Exception as e:
                logging.warning("Error while executing SQL script in database %s: %s" % (self.dbname, e.message))

        sys.exit()
        return None
