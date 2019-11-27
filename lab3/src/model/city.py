from settings import is_valid_str
from model import BaseModel


class City:
    def __init__(self, name: str, c_id: int = None):
        self.id = c_id
        self.name = name

    def __str__(self):
        return f"City [id={self.id}, name={self.name}]"

    @property
    def __dict__(self):
        return {'id': self.id, 'name': self.name}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name[:255]


class CityModel(BaseModel):
    def __init__(self, connection):
        insert_query = "INSERT INTO cities (name) VALUES (%(name)s) RETURNING id"
        select_query = "SELECT * FROM cities WHERE id = %s"
        update_query = "UPDATE cities SET name = %(name)s WHERE id = %(id)s"
        delete_query = "DELETE FROM cities WHERE id = %s"
        select_all_query = "SELECT * FROM cities ORDER BY id OFFSET %(offset)s LIMIT %(limit)s"
        count_query = "SELECT COUNT(*) FROM cities"
        primary_key_name = "id"
        super().__init__(connection, insert_query, select_query, update_query,
                         delete_query, select_all_query, count_query, primary_key_name)

    def _is_valid_item_dict(self, item: dict, pk_required: bool = True):
        return is_valid_str(item['name']) and super()._is_valid_item_dict(item, pk_required)

    @staticmethod
    def _get_item_from_row(row: dict):
        return City(row['name'], row['id'])
