from view import BaseView
from model.invoice import Invoice


class InvoiceView(BaseView):
    @staticmethod
    def show_item(item: object):
        pass

    @staticmethod
    def _items_table_header():
        return ' #num | dep date  | arr date  | cost, ₴  | send#ipn| recp#ipn| w d#num| w a#num|'

    @staticmethod
    def _table_row_from_item(item: object):
        if not isinstance(item, Invoice):
            raise Exception('Item was not a type of Invoice')
        item_date_arrival = f'{item.date_arrival.strftime("%d.%m.%Y")}' if item.date_arrival is not None else 'NULL'
        return f' {item.num:5}| {item.date_departure.strftime("%d.%m.%Y")}| {item_date_arrival:10}|' \
               f' {item.shipping_cost:9}| {item.sender_ipn:8}| {item.recipient_ipn:8}|' \
               f' {item.warehouse_dep_num:7}| {item.warehouse_arr_num:7}|'
