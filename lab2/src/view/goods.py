from view import BaseView
from model.goods import Goods


class GoodsView(BaseView):
    @staticmethod
    def show_item(item: object):
        pass

    @staticmethod
    def _table_head():
        return ' #id     | height,mm| width,mm| depth,mm| weight,mg| description      | inv#num|'

    @staticmethod
    def _item_as_row(item: object):
        if not isinstance(item, Goods):
            raise Exception('Item was not a type of Goods')
        item_description = item.description if item.description is not None else 'NULL'
        return f' {item.id:8}| {item.height:9}| {item.width:8}| {item.depth:8}| {item.weight:9}|' \
               f' {item_description:17}| {item.invoice_num:7}|'
