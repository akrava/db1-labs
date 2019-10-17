from controller import BaseController
from model.contragent import ContragentModel
from view.contragent import ContragentView


class ContragentController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(ContragentModel(connection), ContragentView('contragents', view_driver))

    @staticmethod
    def _prompt_for_item_attributes():
        pass

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        pass
