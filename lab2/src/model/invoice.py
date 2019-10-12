from datetime import date
from decimal import Decimal
from model import BaseModel


class Invoice:
    def __init__(self, date_departure: date, shipping_cost: Decimal, sender_ipn: int, recipient_ipn: int,
                 warehouse_dep_num: int, warehouse_arr_num: int, date_arrival: date = None, num: int = None):
        self.num = num
        self.date_departure = date_departure
        self.date_arrival = date_arrival
        self.shipping_cost = shipping_cost
        self.sender_ipn = sender_ipn
        self.recipient_ipn = recipient_ipn
        self.warehouse_dep_num = warehouse_dep_num
        self.warehouse_arr_num = warehouse_arr_num

    def __str__(self):
        return f"Invoice [num={self.num}, date_departure={self.date_departure}, date_arrival={self.date_arrival}, " \
               f"shipping_cost={self.shipping_cost}, sender_ipn={self.sender_ipn}, " \
               f"recipient_ipn={self.recipient_ipn}, warehouse_dep_num={self.warehouse_dep_num}, " \
               f"warehouse_arr_num={self.warehouse_arr_num}]"


class InvoiceModel(BaseModel):
    def __init__(self, connection):
        insert_query = "INSERT INTO invoices (date_departure, date_arrival, shipping_cost, " \
                       "sender_ipn, recipient_ipn, warehouse_dep_num, warehouse_arr_num) " \
                       "VALUES (%(date_departure)s, %(date_arrival)s, %(shipping_cost)s, " \
                       "%(sender_ipn)s, %(recipient_ipn)s, %(warehouse_dep_num)s, %(warehouse_arr_num)s) " \
                       "RETURNING num"
        select_query = "SELECT *, shipping_cost::numeric as shipping_cost_num FROM invoices WHERE num = %s"
        update_query = "UPDATE invoices SET date_departure = %(date_departure)s, " \
                       "date_arrival = %(date_arrival)s, shipping_cost = %(shipping_cost)s, " \
                       "sender_ipn = %(sender_ipn)s, recipient_ipn = %(recipient_ipn)s, " \
                       "warehouse_dep_num = %(warehouse_dep_num)s, warehouse_arr_num = %(warehouse_arr_num)s " \
                       "WHERE num = %(num)s"
        delete_query = "DELETE FROM invoices WHERE num = %s"
        select_all_query = "SELECT *, shipping_cost::numeric as shipping_cost_num FROM invoices " \
                           "ORDER BY num OFFSET %(offset)s LIMIT %(limit)s"
        count_query = "SELECT COUNT(*) FROM invoices"
        primary_key_name = "num"
        super().__init__(connection, insert_query, select_query, update_query,
                         delete_query, select_all_query, count_query, primary_key_name)
        self.__select_all_with_join_query = ""
        self.__select_with_join_query = ""

    @staticmethod
    def __get_item_from_row(row: dict):
        return Invoice(row['date_departure'], row['shipping_cost_num'], row['sender_ipn'], row['recipient_ipn'],
                       row['warehouse_dep_num'], row['warehouse_arr_num'], row['date_arrival'], row['num'])

    def _is_valid_item_dict(self, item: dict, pk_required: bool = True):
        return all(isinstance(item[column], int) for column in ['sender_ipn', 'recipient_ipn',
                                                                'warehouse_dep_num', 'warehouse_arr_num']) \
               and isinstance(item['date_arrival'], (type(None), date)) and isinstance(item['date_departure'], date) \
               and isinstance(item['shipping_cost_num'], Decimal) \
               and super()._is_valid_item_dict(item, pk_required)
