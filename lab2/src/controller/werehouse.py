from controller import BaseController
from model.warehouse import WarehouseModel
from view.warehouse import WarehouseView


class WarehouseController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(WarehouseModel(connection), WarehouseView('warehouses', view_driver))

    @staticmethod
    def _prompt_for_item_attributes():
        pass

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        pass
