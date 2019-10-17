from psycopg2.extras import DictCursor
from os import path


class Model:
    def __init__(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor(cursor_factory=DictCursor)

    def __del__(self):
        self.__cursor.close()

    def create_tables(self):
        file_path = path.join(path.dirname(path.abspath(__file__)), '../create_tables.sql')
        with open(file_path, 'r') as f:
            sql = f.read()
        self.__cursor.execute(sql)
        self.__connection.commit()

    def truncate_tables(self):
        self.__cursor.execute('TRUNCATE ONLY cities, contragents, goods, '
                              'invoices, warehouses RESTART IDENTITY CASCADE')
        self.__connection.commit()

    def drop_tables(self):
        self.__cursor.execute('DROP TABLE IF EXISTS cities, contragents, '
                              'goods, invoices, warehouses CASCADE')
        self.__connection.commit()
