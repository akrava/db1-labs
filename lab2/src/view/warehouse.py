from view import BaseView
from model.warehouse import Warehouse


class WarehouseView(BaseView):
    @staticmethod
    def show_item(item: object):
        pass

    @staticmethod
    def _table_head():
        return ' #num  | address                         | phone number   | city #id |'

    @staticmethod
    def _item_as_row(item: object):
        if not isinstance(item, Warehouse):
            raise Exception('Item was not a type of Warehouse')
        return f' {item.num:6}| {item.address:32}| {item.phone_number}| {item.city_id:9}|'
