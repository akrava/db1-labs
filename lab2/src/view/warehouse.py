from view import BaseView
from model.warehouse import Warehouse


class WarehouseView(BaseView):
    @staticmethod
    def show_item(item: object):
        pass

    @staticmethod
    def _items_table_header():
        return ' #num  | address                         | phone number   | city #id |'

    @staticmethod
    def _table_row_from_item(item: object):
        if not isinstance(item, Warehouse):
            raise Exception('Item was not a type of Warehouse')
        return f' {item.num:6}| {item.address:32.32}| {item.phone_number}| {item.city_id:9}|'
