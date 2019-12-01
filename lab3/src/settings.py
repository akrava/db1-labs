from dotenv import load_dotenv, find_dotenv
from enum import IntEnum
import logging
import os
import sys

load_dotenv(find_dotenv())


class ConsoleCommands(IntEnum):
    STANDBY = sys.maxsize
    PREV_PAGE = sys.maxsize - 1
    NEXT_PAGE = sys.maxsize - 2
    GO_BACK = sys.maxsize - 3
    CONFIRM = sys.maxsize - 4


class MessageType(IntEnum):
    INFO = 0
    SUCCESSFUL = 1
    ERROR = 2


def setup_db_logging():
    handler_sql = logging.FileHandler('db.log')
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.INFO)
    sql_logger.addHandler(handler_sql)
    sql_logger.propagate = False


DB_DIALECT = "postgresql"
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
