from controller import BaseController
from model.invoice import InvoiceModel
from view.invoice import InvoiceView


class InvoiceController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(InvoiceModel(connection), InvoiceView('invoices', view_driver))

    @staticmethod
    def _prompt_for_item_attributes():
        pass

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        pass
