from view import BaseView
from model.city import City


class CityView(BaseView):
    @staticmethod
    def _table_head():
        return ' #id   | name                |'

    @staticmethod
    def _item_as_row(item: object):
        if not isinstance(item, City):
            raise Exception('Item was not a type of City')
        return f' {item.id:6}| {item.name:20}|'
