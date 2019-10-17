from view import BaseView
from model.invoice import Invoice


class InvoiceView(BaseView):
    @staticmethod
    def show_item(item: object):
        pass

    @staticmethod
    def _table_head():
        return ' #num | dep date  | arr date  | cost, ₴  | send#ipn| recp#ipn| w d#num| w a#num|'

    @staticmethod
    def _item_as_row(item: object):
        if not isinstance(item, Invoice):
            raise Exception('Item was not a type of Invoice')
        item_date_arrival = f'{item.date_arrival}' if item.date_arrival is not None else 'NULL'
        return f' {item.num:5}| {item.date_departure}| {item_date_arrival:10}| {item.shipping_cost:9}|' \
               f' {item.sender_ipn:8}| {item.recipient_ipn:8}|' \
               f' {item.warehouse_dep_num:7}| {item.warehouse_arr_num:7}|'
