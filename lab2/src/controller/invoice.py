from controller import BaseController
from model.invoice import InvoiceModel
from view.invoice import InvoiceView


class InvoiceController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(InvoiceModel(connection), InvoiceView('invoices', view_driver))
