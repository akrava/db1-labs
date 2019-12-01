from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Base


class Model:
    def __init__(self, dialect: str, host: str, port: int, db_name: str, user: str, password: str):
        self.__engine = create_engine(f"{dialect}://{user}:{password}@{host}:{port}/{db_name}")
        session_class = sessionmaker(bind=self.__engine)
        self.__session = session_class()

    def session(self):
        return self.__session

    def create_tables(self):
        Base.metadata.create_all(self.__engine)

    def truncate_tables(self):
        pass
        # self.__cursor.execute('TRUNCATE ONLY cities, contragents, goods, '
        #                       'invoices, warehouses RESTART IDENTITY CASCADE')
        # self.__connection.commit()

    def drop_tables(self):
        Base.metadata.drop_all(self.__engine)

    def filter_items(self, cost_from: int, cost_to: int, sender_name: str = None, recipient_name: str = None):
        pass
        # query = "SELECT num, date_departure, date_arrival, shipping_cost, c1.name, " \
        #         "c1.phone_number, c2.name, c2.phone_number from invoices i " \
        #         "INNER JOIN contragents c1 on i.sender_ipn = c1.ipn " \
        #         "INNER JOIN contragents c2 on i.recipient_ipn = c2.ipn " \
        #         "WHERE " \
        #         "shipping_cost::numeric BETWEEN (%(min)s) AND (%(max)s)"
        # if isinstance(sender_name, str):
        #     query += " AND c1.name = (%(sender)s)"
        # if isinstance(recipient_name, str):
        #     query += " AND c2.name = (%(recipient)s)"
        # self.__cursor.execute(query, {'min': cost_from, 'max': cost_to,
        #                               'sender': sender_name, 'recipient': recipient_name})
        # rows = self.__cursor.fetchall()
        # if isinstance(rows, list):
        #     return rows
        # else:
        #     raise Exception("There are no items")

    def fulltext_search(self, query: str, including: bool):
        pass
        # if not including:
        #     words = query.split()
        #     if len(words) > 0:
        #         words[0] = "!" + words[0]
        #     counter = 1
        #     while counter < len(words):
        #         words[counter] = "& !" + words[counter]
        #     query = ' '.join(words)
        # query_excluding = "SELECT ts_headline(description, q) " \
        #                   "FROM goods, to_tsquery('english', %(query)s) AS q " \
        #                   "WHERE to_tsvector('english', description) @@ q "
        # query_including = "SELECT ts_headline(description, q) " \
        #                   "FROM goods, plainto_tsquery('english', %(query)s) AS q " \
        #                   "WHERE to_tsvector('english', description) @@ q "
        # self.__cursor.execute(query_including if including else query_excluding, {'query': query})
        # rows = self.__cursor.fetchall()
        # if isinstance(rows, list):
        #     return rows
        # else:
        #     raise Exception("There are no items")
