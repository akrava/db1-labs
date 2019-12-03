from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import asc
from typing import Type

Base = declarative_base()


class Model:
    def __init__(self, session: Session, cls: Type):
        self.__session = session
        self._cls = cls

    def create(self, item: object):
        self.__session.add(item)
        self.__commit_or_rollback_on_failure()
        return item

    def create_many(self, items: [object]):
        self.__session.add_all(items)
        self.__commit_or_rollback_on_failure()
        return items

    def read(self, pk: int):
        item = self.__session.query(self._cls).get(pk)
        if item is None:
            raise Exception(f"No item with such primary key {pk} was found")
        return item

    def read_all(self, offset: int = 0, limit: int = None):
        pk_name = self.get_primary_key_name()
        items = self.__session.query(self._cls).order_by(asc(pk_name)).offset(offset).limit(limit).all()
        return items

    def count_all(self):
        return self.__session.query(self._cls).count()

    def update(self, item: dict):
        pk_name = self.get_primary_key_name()
        pk = item[pk_name]
        try:
            self.__session.query(self._cls).filter_by(**{pk_name: pk}).update(item)
            self.__session.commit()
        except Exception:
            self.__session.rollback()
            raise
        return self.read(pk)

    def delete(self, pk: int):
        pk_name = self.get_primary_key_name()
        try:
            self.__session.query(self._cls).filter_by(**{pk_name: pk}).delete()
            self.__session.commit()
        except Exception:
            self.__session.rollback()
            raise

    def __commit_or_rollback_on_failure(self):
        try:
            self.__session.commit()
        except Exception:
            self.__session.rollback()
            raise

    @staticmethod
    def get_primary_key_value(item: object):
        return inspect(item).identity[0]

    def get_primary_key_name(self):
        return inspect(self._cls).primary_key[0].name
