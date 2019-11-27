from settings import is_valid_str
from model import BaseModel


class Warehouse:
    def __init__(self, address: str, phone_number: str, city_id: int, num: int = None):
        self.num = num
        self.address = address
        self.phone_number = phone_number
        self.city_id = city_id

    def __str__(self):
        return f"Warehouse [num={self.num}, address={self.address}, " \
               f"phone_number={self.phone_number}, city_id={self.city_id}]"

    @property
    def __dict__(self):
        return {'num': self.num, 'address': self.address,
                'phone_number': self.phone_number, 'city_id': self.city_id}

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number: str):
        self.__phone_number = phone_number[:15]


class WarehouseModel(BaseModel):
    def __init__(self, connection):
        insert_query = "INSERT INTO warehouses (address, phone_number, city_id) " \
                       "VALUES (%(address)s, %(phone_number)s, %(city_id)s) RETURNING num"
        select_query = "SELECT * FROM warehouses WHERE num = %s"
        update_query = "UPDATE warehouses SET address = %(address)s, " \
                       "phone_number = %(phone_number)s, city_id = %(city_id)s " \
                       "WHERE num = %(num)s"
        delete_query = "DELETE FROM warehouses WHERE num = %s"
        select_all_query = "SELECT * FROM warehouses ORDER BY num OFFSET %(offset)s LIMIT %(limit)s"
        count_query = "SELECT COUNT(*) FROM warehouses"
        primary_key_name = "num"
        super().__init__(connection, insert_query, select_query, update_query,
                         delete_query, select_all_query, count_query, primary_key_name)

    def _is_valid_item_dict(self, item: dict, pk_required: bool = True):
        return isinstance(item['city_id'], int) and is_valid_str(item['address']) \
               and is_valid_str(item['phone_number']) \
               and super()._is_valid_item_dict(item, pk_required)

    @staticmethod
    def _get_item_from_row(row: dict):
        return Warehouse(row['address'], row['phone_number'], row['city_id'], row['num'])
