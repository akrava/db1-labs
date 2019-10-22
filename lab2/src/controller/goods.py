from controller import BaseController
from model.goods import GoodsModel, Goods
from view.goods import GoodsView


class GoodsController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(GoodsModel(connection), GoodsView('goods', view_driver))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Height (mm)', 'Width (mm)', 'Depth (mm)',
                   'Weight (g)', 'Description (could be empty)', 'Invoice number']
        values = [item.height, item.width, item.depth, item.weight, item.description,
                  item.invoice_num] if isinstance(item, Goods) else None
        return prompts, values

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
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
        return Goods(height, width, depth, weight, invoice_number, description)
