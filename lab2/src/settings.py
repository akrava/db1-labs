import os
import sys
from enum import IntEnum
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class ConsoleCommands(IntEnum):
    GO_BACK = sys.maxsize
    PREV_PAGE = sys.maxsize - 1
    NEXT_PAGE = sys.maxsize - 2


class MessageType(IntEnum):
    INFO = 0
    SUCCESSFUL = 1
    ERROR = 2


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
