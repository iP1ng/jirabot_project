# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname

with open(join(dirname(__file__), 'docs/readme.rst')) as f:
    readme = f.read()

with open(join(dirname(__file__), 'LICENSE')) as f:
    license = f.read()

POSTGRESQL_REQUIRES = [
    'psycopg2 > 2.7.3'
]

JIRA_REQUIRES = [
    'jira > 1.0.10'
]

setup(
    name='jirabot',
    version='0.1.0',
    description='Automation of purchasing data from PostgreSQL via Jira interface',
    long_description=readme,
    author='Anatoly Soldatov',
    author_email='a.k.soldatov@gmail.com',
    url='https://github.com/yum-install-brains/jirabot_project',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'logs')),
    extras_require={
          'postgresql': POSTGRESQL_REQUIRES,
          'jira': JIRA_REQUIRES,
      },
    test_suite=join(dirname(__file__), 'tests/tests'),
    entry_points={
        'console_scripts':
            ['jirabot = jirabot:run']
        }
)
