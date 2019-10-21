from psycopg2.extras import DictCursor
from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, connection, insert_query, select_query, update_query,
                 delete_query, select_all_query, count_query, primary_key_name):
        self._connection = connection
        self._cursor = connection.cursor(cursor_factory=DictCursor)
        self.__insert_query = insert_query
        self.__select_query = select_query
        self.__update_query = update_query
        self.__delete_query = delete_query
        self.__select_all_query = select_all_query
        self.__count_query = count_query
        self.__primary_key_name = primary_key_name

    def __del__(self):
        self._cursor.close()

    def rollback(self):
        self._connection.rollback()

    @property
    def primary_key_name(self):
        return self.__primary_key_name

    def create(self, item: object):
        should_return_id = "returning" in self.__insert_query.lower()
        if not self._is_valid_item_dict(item.__dict__, not should_return_id):
            raise Exception("Item is not valid")
        self._cursor.execute(self.__insert_query, item.__dict__)
        self._connection.commit()
        if should_return_id:
            row = self._cursor.fetchone()
            if row is not None and isinstance(row[self.__primary_key_name], int):
                self.__insert_pk_in_item(item, row[self.__primary_key_name])
                return item
            else:
                raise Exception("No rows received from DB")

    def create_many(self, items: [object], get_ids: bool = False):
        should_return_id = "returning" in self.__insert_query.lower()
        if should_return_id and get_ids:
            for item in items:
                self.create(item)
            return items
        else:
            if any(not self._is_valid_item_dict(item.__dict__, not should_return_id) for item in items):
                raise Exception("Item is not valid")
            self._cursor.executemany(self.__insert_query, [item.__dict__ for item in items])
            self._connection.commit()

    def read(self, pk: int):
        if not isinstance(pk, int):
            raise Exception("Primary key should be an integer")
        self._cursor.execute(self.__select_query, [pk])
        row = self._cursor.fetchone()
        if row is not None and self._is_valid_item_dict(row):
            return self._get_item_from_row(row)
        else:
            raise Exception(f"No item with such primary key {pk} was found")

    def read_all(self, offset: int = 0, limit: int = None):
        self._cursor.execute(self.__select_all_query, {'limit': limit, 'offset': offset})
        rows = self._cursor.fetchall()
        if isinstance(rows, list) and all(self._is_valid_item_dict(row) for row in rows):
            return [self._get_item_from_row(row) for row in rows]
        else:
            raise Exception("There are no items")

    def count_all(self):
        self._cursor.execute(self.__count_query)
        row = self._cursor.fetchone()
        if row is not None and isinstance(row['count'], int):
            return row['count']
        else:
            raise Exception("No rows received from DB")

    def update(self, item: object):
        if not self._is_valid_item_dict(item.__dict__):
            raise Exception("Item is not valid")
        self._cursor.execute(self.__update_query, item.__dict__)
        self._connection.commit()

    def delete(self, pk: int):
        if not isinstance(pk, int):
            raise Exception("Primary key should be an integer")
        self._cursor.execute(self.__delete_query, [pk])
        self._connection.commit()

    def _is_valid_item_dict(self, item: dict, pk_required: bool = True):
        if pk_required:
            return isinstance(item[self.__primary_key_name], int)
        else:
            return item[self.__primary_key_name] is None

    @staticmethod
    @abstractmethod
    def _get_item_from_row(row: dict):
        pass

    def __insert_pk_in_item(self, item: object, pk: int):
        setattr(item, self.__primary_key_name, pk)
