from controller import BaseController
from sqlalchemy.orm import Session
from view.goods import GoodsView
from model.goods import Goods
from view.common import View


class GoodsController(BaseController):
    def __init__(self, session: Session, view: View):
        super().__init__(session, Goods, GoodsView('goods', view))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Height (mm)', 'Width (mm)', 'Depth (mm)',
                   'Weight (g)', 'Description (could be empty)', 'Invoice number']
        values = [item.height, item.width, item.depth, item.weight, item.description,
                  item.invoice_num] if isinstance(item, Goods) else None
        return prompts, values

    @staticmethod
    def _create_dict_from_input(input_items: [dict]):
        height = width = depth = weight = description = invoice_number = None
        for item in input_items:
            if item['name'] != 'Description (could be empty)' and int(item['value']) <= 0:
                raise Exception(f"{item['name']} should be > 0, got {int(item['value'])}")
            if item['name'] == 'Height (mm)':
                height = int(item['value'])
            elif item['name'] == 'Width (mm)':
                width = int(item['value'])
            elif item['name'] == 'Depth (mm)':
                depth = int(item['value'])
            elif item['name'] == 'Weight (g)':
                weight = int(item['value'])
            elif item['name'] == 'Description (could be empty)':
                description = item['value']
            elif item['name'] == 'Invoice number':
                invoice_number = int(item['value'])
        return dict(height=height, width=width, depth=depth, weight=weight, description=description,
                    invoice_num=invoice_number)
