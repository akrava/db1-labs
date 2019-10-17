from view import BaseView
from model.contragent import Contragent


class ContragentView(BaseView):
    @staticmethod
    def show_item(item: object):
        pass

    @staticmethod
    def _table_head():
        return ' #ipn      | name                | phone number   |'

    @staticmethod
    def _item_as_row(item: object):
        if not isinstance(item, Contragent):
            raise Exception('Item was not a type of Contragent')
        return f' {item.ipn:10}| {item.name:20}| {item.phone_number}|'
