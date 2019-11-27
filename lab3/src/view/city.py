from view import BaseView
from model.city import City


class CityView(BaseView):
    @staticmethod
    def _item_to_text(item: object):
        if not isinstance(item, City):
            raise Exception('Item was not a type of City')
        return f'Name: {item.name}\nID: {item.id}'

    @staticmethod
    def _items_table_header():
        return ' #id   | name                |'

    @staticmethod
    def _table_row_from_item(item: object):
        if not isinstance(item, City):
            raise Exception('Item was not a type of City')
        return f' {item.id:6}| {item.name:20.20}|'
