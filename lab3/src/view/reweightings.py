from view import BaseView
from model.reweightings import Reweightings


class ReweightingsView(BaseView):
    @staticmethod
    def _item_to_text(item: object):
        if not isinstance(item, Reweightings):
            raise Exception('Item was not a type of Reweightings')
        return f'ID: {item.id}\nDate inspection: {item.date_inspection.strftime("%d.%m.%Y %H:%M:%S")}\n' \
               f'Weight before: {item.weight_before} g\nWeight after: {item.weight_after} g\n' \
               f'Parcel ID (goods.id): {item.parcel_id}'

    @staticmethod
    def _items_table_header():
        return ' #id  | date inspection    | weight before, g | weight after, g | goods#id |'

    @staticmethod
    def _table_row_from_item(item: object):
        if not isinstance(item, Reweightings):
            raise Exception('Item was not a type of Reweightings')
        return f' {item.id:5}| {item.date_inspection.strftime("%d.%m.%Y %H:%M:%S"):19.19}|' \
               f' {item.weight_before:17}| {item.weight_after:16}| {item.parcel_id:9}|'
