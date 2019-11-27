from psycopg2.extras import DictCursor
from os import path


class Model:
    def __init__(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor(cursor_factory=DictCursor)

    def __del__(self):
        self.__cursor.close()

    def rollback(self):
        self.__connection.rollback()

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

    def filter_items(self, cost_from: int, cost_to: int, sender_name: str = None, recipient_name: str = None):
        query = "SELECT num, date_departure, date_arrival, shipping_cost, c1.name, " \
                "c1.phone_number, c2.name, c2.phone_number from invoices i " \
                "INNER JOIN contragents c1 on i.sender_ipn = c1.ipn " \
                "INNER JOIN contragents c2 on i.recipient_ipn = c2.ipn " \
                "WHERE " \
                "shipping_cost::numeric BETWEEN (%(min)s) AND (%(max)s)"
        if isinstance(sender_name, str):
            query += " AND c1.name = (%(sender)s)"
        if isinstance(recipient_name, str):
            query += " AND c2.name = (%(recipient)s)"
        self.__cursor.execute(query, {'min': cost_from, 'max': cost_to,
                                      'sender': sender_name, 'recipient': recipient_name})
        rows = self.__cursor.fetchall()
        if isinstance(rows, list):
            return rows
        else:
            raise Exception("There are no items")

    def fulltext_search(self, query: str, including: bool):
        if not including:
            words = query.split()
            if len(words) > 0:
                words[0] = "!" + words[0]
            counter = 1
            while counter < len(words):
                words[counter] = "& !" + words[counter]
            query = ' '.join(words)
        query_excluding = "SELECT ts_headline(description, q) " \
                          "FROM goods, to_tsquery('english', %(query)s) AS q " \
                          "WHERE to_tsvector('english', description) @@ q "
        query_including = "SELECT ts_headline(description, q) " \
                          "FROM goods, plainto_tsquery('english', %(query)s) AS q " \
                          "WHERE to_tsvector('english', description) @@ q "
        self.__cursor.execute(query_including if including else query_excluding, {'query': query})
        rows = self.__cursor.fetchall()
        if isinstance(rows, list):
            return rows
        else:
            raise Exception("There are no items")
