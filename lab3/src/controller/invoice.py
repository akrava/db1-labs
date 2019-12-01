from controller import BaseController
from view.invoice import InvoiceView
from sqlalchemy.orm import Session
from model.invoice import Invoice
from datetime import datetime
from view.common import View
from decimal import Decimal


class InvoiceController(BaseController):
    def __init__(self, session: Session, view: View):
        super().__init__(session, Invoice, InvoiceView('invoices', view))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Date departure (DD.MM.YYYY)', 'Date arrival (DD.MM.YYYY, could be empty)',
                   'Shipping cost (₴)', 'Sender IPN', 'Recipient IPN',
                   'Warehouse departure number', 'Warehouse arrival number']
        values = [item.date_departure.strftime("%d.%m.%Y"),
                  item.date_arrival.strftime("%d.%m.%Y") if item.date_arrival is not None else None,
                  item.shipping_cost, item.sender_ipn, item.recipient_ipn, item.warehouse_dep_num,
                  item.warehouse_arr_num] if isinstance(item, Invoice) else None
        return prompts, values

    @staticmethod
    def _create_dict_from_input(input_items: [dict]):
        date_departure = date_arrival = shipping_cost = sender_ipn \
            = recipient_ipn = warehouse_dep_num = warehouse_arr_num = None
        for item in input_items:
            value = item['value']
            if item['name'] == 'Date departure (DD.MM.YYYY)':
                date_departure = datetime.strptime(value, "%d.%m.%Y").date()
            elif item['name'] == 'Date arrival (DD.MM.YYYY, could be empty)':
                date_arrival = datetime.strptime(value, "%d.%m.%Y").date() if item['value'] is not None else None
            elif item['name'] == 'Shipping cost (₴)':
                shipping_cost = Decimal(value)
                if shipping_cost <= 0:
                    raise Exception(f"Shipping cost should be > 0, got {shipping_cost}")
            elif item['name'] == 'Sender IPN':
                sender_ipn = int(value)
            elif item['name'] == 'Recipient IPN':
                recipient_ipn = int(value)
            elif item['name'] == 'Warehouse departure number':
                warehouse_dep_num = int(value)
            elif item['name'] == 'Warehouse arrival number':
                warehouse_arr_num = int(value)
        return dict(date_departure=date_departure, shipping_cost=shipping_cost, sender_ipn=sender_ipn,
                    recipient_ipn=recipient_ipn, warehouse_dep_num=warehouse_dep_num,
                    warehouse_arr_num=warehouse_arr_num, date_arrival=date_arrival)
