from psycopg2.extras import DictCursor
import logging


class BaseModel:
    def __init__(self, connection):
        self._connection = connection
        self._cursor = connection.cursor(cursor_factory=DictCursor)

    def __del__(self):
        self._cursor.close()
        logging.info("BaseModel closed cursor")
