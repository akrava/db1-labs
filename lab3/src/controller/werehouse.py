from view.warehouse import WarehouseView
from controller import BaseController
from model.warehouse import Warehouse
from sqlalchemy.orm import Session
from view.common import View


class WarehouseController(BaseController):
    def __init__(self, session: Session, view: View):
        super().__init__(session, Warehouse, WarehouseView('warehouses', view))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Address', 'Phone number', 'City ID']
        values = [item.address, item.phone_number, item.city_id] \
            if isinstance(item, Warehouse) else None
        return prompts, values

    @staticmethod
    def _create_dict_from_input(input_items: [dict]):
        address = phone_number = city_id = None
        for item in input_items:
            if item['name'] == 'Address':
                address = item['value']
            elif item['name'] == 'Phone number':
                phone_number = item['value']
            elif item['name'] == 'City ID':
                city_id = int(item['value'])
        return dict(address=address, phone_number=phone_number, city_id=city_id)
