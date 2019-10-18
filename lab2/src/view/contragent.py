from view import BaseView
from model.contragent import Contragent


class ContragentView(BaseView):
    @staticmethod
    def show_item(item: object):
        pass

    @staticmethod
    def _items_table_header():
        return ' #ipn      | name                | phone number   |'

    @staticmethod
    def _table_row_from_item(item: object):
        if not isinstance(item, Contragent):
            raise Exception('Item was not a type of Contragent')
        return f' {item.ipn:10}| {item.name:20.20}| {item.phone_number}|'
