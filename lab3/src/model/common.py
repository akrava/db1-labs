from sqlalchemy.orm import sessionmaker, close_all_sessions
from sqlalchemy import create_engine, MetaData, func, text
from model.invoice import Invoice
from model.goods import Goods
from model import Base
from os import path


class Model:
    def __init__(self, dialect: str, host: str, port: int, db_name: str, user: str, password: str):
        self.__engine = create_engine(f"{dialect}://{user}:{password}@{host}:{port}/{db_name}")
        session_class = sessionmaker(bind=self.__engine)
        self.__session = session_class()

    def __del__(self):
        self.__session.commit()
        close_all_sessions()

    def session(self):
        return self.__session

    def create_tables(self):
        # close_all_sessions()
        Base.metadata.create_all(self.__engine)
        file_path = path.join(path.dirname(path.abspath(__file__)), '../goods_trigger.sql')
        with open(file_path, 'r') as f:
            sql = f.read()
        self.__session.execute(text(sql))
        self.__session.commit()

    def truncate_tables(self):
        meta = MetaData(bind=self.__engine, reflect=True)
        for tbl in reversed(meta.sorted_tables):
            self.__session.execute(tbl.delete())
            self.__session.commit()

    def drop_tables(self):
        close_all_sessions()
        Base.metadata.drop_all(self.__engine)

    def filter_items(self, cost_from: int, cost_to: int, sender_name: str = None, recipient_name: str = None):
        query = self.__session.query(Invoice).filter(Invoice.shipping_cost.between(cost_from, cost_to))
        if isinstance(sender_name, str):
            query = query.filter(Invoice.sender.has(name=sender_name))
        if isinstance(recipient_name, str):
            query = query.filter(Invoice.recipient.has(name=recipient_name))
        return query.all()

    def fulltext_search(self, query: str, including: bool):
        """
        SELECT id, ts_headline(description, q) FROM (
            SELECT id, description, q
                FROM goods, to_tsquery('english', 'query & here') q
                WHERE to_tsvector('english', description) @@ q
        ) search_t;
        """
        query = self.__prepare_query(query, including)
        q = func.to_tsquery('english', query)
        inner_statement = self.__session \
            .query(Goods.id, Goods.description, q) \
            .select_from(q) \
            .filter(func.to_tsvector('english', Goods.description).match(query, postgresql_regconfig='english')) \
            .subquery()
        return self.__session.query(inner_statement.c.id, func.ts_headline(inner_statement.c.description, q)).all()

    @staticmethod
    def __prepare_query(query: str, including: bool):
        words = query.split()
        if len(words) > 0 and not including:
            words[0] = "!" + words[0]
        counter = 1
        while counter < len(words):
            words[counter] = f"& {'!' if not including else ''}" + words[counter]
            counter += 1
        return ' '.join(words)
