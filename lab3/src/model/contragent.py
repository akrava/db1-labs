from settings import is_valid_str
from model import BaseModel


class Contragent:
    def __init__(self, ipn: int, name: str, phone_number: str):
        self.ipn = ipn
        self.name = name
        self.phone_number = phone_number

    def __str__(self):
        return f"Contragent [ipn={self.ipn}, name={self.name}, phone_number={self.phone_number}]"

    @property
    def __dict__(self):
        return {'ipn': self.ipn, 'name': self.name, 'phone_number': self.phone_number}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name[:255]

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number: str):
        self.__phone_number = phone_number[:15]


class ContragentModel(BaseModel):
    def __init__(self, connection):
        insert_query = "INSERT INTO contragents (ipn, name, phone_number) " \
                       "VALUES (%(ipn)s, %(name)s, %(phone_number)s)"
        select_query = "SELECT * FROM contragents WHERE ipn = %s"
        update_query = "UPDATE contragents SET name = %(name)s, phone_number = %(phone_number)s " \
                       "WHERE ipn = %(ipn)s"
        delete_query = "DELETE FROM contragents WHERE ipn = %s"
        select_all_query = "SELECT * FROM contragents ORDER BY ipn OFFSET %(offset)s LIMIT %(limit)s"
        count_query = "SELECT COUNT(*) FROM contragents"
        primary_key_name = "ipn"
        super().__init__(connection, insert_query, select_query, update_query,
                         delete_query, select_all_query, count_query, primary_key_name)

    def get_distinct_names(self):
        query = "SELECT DISTINCT name from contragents"
        self._cursor.execute(query)
        rows = self._cursor.fetchall()
        if isinstance(rows, list) and all(is_valid_str(row['name']) for row in rows):
            return [row['name'] for row in rows]
        else:
            raise Exception("There are no items")

    def _is_valid_item_dict(self, item: dict, pk_required: bool = True):
        return all(is_valid_str(item[column]) for column in ['name', 'phone_number']) \
               and super()._is_valid_item_dict(item, pk_required)

    @staticmethod
    def _get_item_from_row(row: dict):
        return Contragent(row['ipn'], row['name'], row['phone_number'])
