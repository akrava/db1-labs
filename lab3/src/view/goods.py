from view import BaseView
from model.goods import Goods


class GoodsView(BaseView):
    @staticmethod
    def _item_to_text(item: object):
        if not isinstance(item, Goods):
            raise Exception('Item was not a type of Goods')
        item_description = item.description if item.description is not None else '<empty>'
        return f'ID: {item.id}\nHeight: {item.height} mm\nWidth: {item.width} mm\n' \
               f'Depth:{item.depth} mm\nWeight: {item.weight} g\n' \
               f'Description: {item_description}\nInvoice number: {item.invoice_num}'

    @staticmethod
    def _items_table_header():
        return ' #id     | height,mm| width,mm| depth,mm| weight, g| description      | inv#num|'

    @staticmethod
    def _table_row_from_item(item: object):
        if not isinstance(item, Goods):
            raise Exception('Item was not a type of Goods')
        item_description = item.description if item.description is not None else '<empty>'
        return f' {item.id:8}| {item.height:9}| {item.width:8}| {item.depth:8}| {item.weight:9}|' \
               f' {item_description:17.17}| {item.invoice_num:7}|'
