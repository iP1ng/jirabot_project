О проекте
===================================

Проект Jirabot призван сократить время выполнения типовых задач по предоставлению информации из базы данных PostgreSQL. Интерфейсом взаимодействия с ботом являются задачи в Jira, заведенные по определенному шаблону. Для работы требуется задать параметры подключения к сервису Jira и базе данных. Также нужно описать шаблоны задач для автоматического выполнения. В настоящий момент находится в бете.

Установка
----------

.. code-block:: bash 

	git clone https://github.com/yum-install-brains/jirabot_project.git
	cd jirabot_project
	python3 setup.py install

Конфигурация
---------------

Настройка Jirabot реализована через конфигурационные файлы:

Параметры подключения к БД по умолчанию задаются в файле jirabot/config/database_credentials.json, но можно хранить их в любом другом месте.

Пример

.. code-block:: javascript

	{
	    "dbconfig1": {
	        "dbuser":"user1",
	        "dbpassword":"password1",
	        "dbname":"database1",
	        "dbhost":"127.0.0.1",
	        "dbport":"5432"
	    },
	    "dbconfig2":{
	        "dbuser":"user2",
	        "dbpassword":"password2",
	        "dbname":"database2",
	        "dbhost":"127.0.0.1",
	        "dbport":"5432"
	    }
	}



Параметры подключения к Jira по умолчанию задаются в файле jirabot/config/jira_credentials.json, но можно хранить их в любом другом месте.

Пример

.. code-block:: javascript

	{
	    "jira_server_1": {
	        "jira_server": "https://jira1.com",
	        "jira_user": "jirabot",
	        "jira_password": "megasecret",
	        "jira_certificate":"certificates/jira1.ca-bundle"
	    },
	    "jira_server_2":{
	        "jira_server": "https://jira2.com",
	        "jira_user": "jirabot",
	        "jira_password": "supersecret",
	        "jira_certificate":"certificates/jira2.ca-bundle"
	    }
	}


Шаблоны задач в Jira по умолчанию задаются в файлах jirabot/tasks/<task_name>.json, но можно хранить их в любом другом месте. Здесь query - запрос для выполнения в БД, результат которого вставляется в виде комментария в задачу. Запрос может содержать динамический предикат, значение параметра будет подставлено из поля задачи, указанного в field. Каждые periodicity секунд Jirabot будет подключаться к Jira серверу с конфигурацией jira и искать все запросы по условию condition. Для каждого найденного запроса будет выполнен query, результат будет приложен в виде комментария в задачу, а задача возвращена на автора.

Пример

.. code-block:: javascript

	{
	      "test": {
	        "jira":"jira_server_1",
	        "database":"dbconfig1",
	        "query":"SELECT 'test1!';",
	        "condition":"assignee = jirabot and summary ~ 'test1'",
	        "periodicity":60,
	        "field":"description"
	    },
	      "test2": {
	        "jira":"jira_server_2",
	        "database":"dbconfig2",
	        "query":"SELECT 'test2!';",
	        "condition":"assignee = jirabot and summary ~ 'test2'",
	        "periodicity":60,
	        "field":"my_custom_field_name"
	    }
	}


Запуск
---------
Запускается из командной строки (с указанием аргументов или без). 
	- Запуск без аргументов - запуск с путем к конфигурационным файлам по умолчанию.
	- Запуск с 1 аргументом - запуск с указанием пути к шаблону задачи.
	- Запуск с пустым сертификатом
	- Запуск с 3 аргументами - запуск с указанием пути к шаблону задачи, а также к конфигурационным файлам подключения к БД и Jira.

Пример

.. code-block:: bash

	cd /<путь к jirabot_project> && jirabot /home/johndoe/tasks/test_task.json

TODO
---------
	- Заменить хардкод путей к сертификатам Jira, добавив дополнительный аргумент в вызов (путь к сертификатам).
	- Указывать путь к необходимому сертификату Jira в конфигурационном файле Jira (к разным Jira разные сертификаты).
	- Добавить описание конфигурационных файлов
	- Добавить телеграм-бота (вместо интерфейса Jira)
	- Добавить поддержку других БД (для начала mysql)
	- Добавить github pages для документации
	- Добавить веб-морду для конфигурации и отслеживания статуса

Обратная связь
---------------

По всем предложениям и найденным багам пишите мне :) 
	- Skype - justbrodwey
 	- Telegram - @AnatolySK (https://t.me/AnatolySK)
 	- email - a.k.soldatov@gmail.com

Для добавления нового шаблона задачи скидывайте мне готовый файл шаблона задачи или добавляйте описание шаблона в гуглдок:
https://docs.google.com/spreadsheets/d/1oiwIdMMfxTNlDjrjcx_FHHLQ6_hXB_jFdieAvPygLe4/edit?usp=sharing