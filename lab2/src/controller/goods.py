from controller import BaseController
from model.goods import GoodsModel
from view.goods import GoodsView


class GoodsController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(GoodsModel(connection), GoodsView('goods', view_driver))

    @staticmethod
    def _prompt_for_item_attributes():
        pass

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        pass
