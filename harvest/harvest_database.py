import psycopg2
import logging.config
import logging
import yaml
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
logger = logging.getLogger(__name__)


def setup_logging(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration from a yaml file.
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            logging_config = yaml.safe_load(f.read())
        logging.config.dictConfig(logging_config)

    else:
        logging.basicConfig(level=default_level)


def create_db(user, password, host, dbname, port):
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database="postgres")
        connection.autocommit = True
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        find_db_query = "SELECT datname FROM pg_catalog.pg_database WHERE datname = '{}';".format(dbname)
        cursor.execute(find_db_query)
        if cursor.fetchone():
            pass
        else:
            create_db_query = "CREATE DATABASE {};".format(dbname)

            cursor.execute(create_db_query)
            connection.commit()
            cursor.close()
            connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


def establish_connection(user, password, host, dbname, port):
    create_db(user, password, host, dbname, port)
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=dbname)
    return connection


def create_table_details(user, password, host, dbname, port):
    try:
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS downloadpages
              (ID SERIAL PRIMARY KEY     NOT NULL,
              Name           VARCHAR    NOT NULL,
              Version        VARCHAR); '''

        cursor.execute(create_table_query)
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


def create_table_links(user, password, host, dbname, port):
    try:
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS downloadlinks
              (ID SERIAL PRIMARY KEY     NOT NULL,
              Link         VARCHAR    NOT NULL); '''

        cursor.execute(create_table_query)
        cursor.close()
        connection.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


def create_table_translations(user, password, host, dbname, port):
    try:
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS downloadtranslations
              (ID SERIAL PRIMARY KEY     NOT NULL,
              Link         VARCHAR    NOT NULL,
              Version      VARCHAR    NOT NULL); '''

        cursor.execute(create_table_query)
        cursor.close()
        connection.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


#  CREATE
def insert_links(user, password, host, dbname, port, link):
    try:
        create_table_links(user, password, host, dbname, port)
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        cursor = connection.cursor()
        insert_query = "INSERT INTO downloadlinks (Link)" \
                       " VALUES(%s)"
        cursor.execute(insert_query, (link,))
        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


def insert_details(user, password, host, dbname, port, dl_dict):
    try:
        create_table_details(user, password, host, dbname, port)
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()
        insert_query = "INSERT INTO downloadpages(Name, Version)" \
                       " VALUES(%(name)s,%(version)s)"
        cursor.execute(insert_query, dl_dict)
        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


def insert_translations(user, password, host, dbname, port, translation_dict):
    try:
        create_table_details(user, password, host, dbname, port)
        connection = establish_connection(user, password, host, dbname, port)

        connection.autocommit = True
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()
        insert_query = "INSERT INTO downloadtranslations(Link, Version)" \
                       " VALUES(%(language)s,%(version)s)"
        cursor.execute(insert_query, translation_dict)
        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


#  READ
def select_links(user, password, host, dbname, port, link):  # check if the link is already in the table 'downloadlinks'
    try:
        create_table_links(user, password, host, dbname, port)
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        cursor = connection.cursor()

        search_query = "SELECT * FROM downloadlinks WHERE Link = '{}'".format(link)
        cursor.execute(search_query)
        result = cursor.fetchone()
        if result is None:
            cursor.close()
            connection.close()
            return True
        else:
            cursor.close()
            connection.close()
            return False
    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


def select_all_links(user, password, host, dbname, port):
    try:
        create_table_links(user, password, host, dbname, port)
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        cursor = connection.cursor()

        search_query = "SELECT * FROM downloadlinks"
        cursor.execute(search_query)
        links_list = [r[1] for r in cursor.fetchall()]
        cursor.close()
        connection.close()
        return links_list
    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


def select_details(user, password, host, dbname, port, detail_dict):
    try:
        create_table_details(user, password, host, dbname, port)
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        cursor = connection.cursor()

        search_query = "SELECT * FROM downloadpages WHERE Name='{}' and Version ='{}'".format(detail_dict["name"],
                                                                                              detail_dict["version"])
        cursor.execute(search_query)
        result = cursor.fetchone()
        if result is None:
            cursor.close()
            connection.close()
            return True
        else:
            cursor.close()
            connection.close()
            return False
    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)


def select_translations(user, password, host, dbname, port, translation_dict):
    try:
        create_table_translations(user, password, host, dbname, port)
        connection = establish_connection(user, password, host, dbname, port)
        connection.autocommit = True
        cursor = connection.cursor()

        search_query = "SELECT * " \
                       "FROM downloadtranslations " \
                       "WHERE Link='{}' and Version ='{}'".format(translation_dict["language"], translation_dict["version"])
        cursor.execute(search_query)
        result = cursor.fetchone()

        if result is None:
            cursor.close()
            connection.close()
            return True
        else:
            cursor.close()
            connection.close()
            return False
    except (Exception, psycopg2.Error) as error:
        logger.error('Error while connecting to PostgreSQL: ' + str(error), exc_info=True)



setup_logging()
