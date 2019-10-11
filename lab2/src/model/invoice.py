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
        super().__init__(connection)
        self.__insert_query = "INSERT INTO invoices (date_departure, date_arrival, shipping_cost, " \
                              "sender_ipn, recipient_ipn, warehouse_dep_num, warehouse_arr_num) " \
                              "VALUES (%(date_departure)s, %(date_arrival)s, %(shipping_cost)s, " \
                              "%(sender_ipn)s, %(recipient_ipn)s, %(warehouse_dep_num)s, %(warehouse_arr_num)s) " \
                              "RETURNING num"
        self.__select_query = "SELECT *, shipping_cost::numeric as shipping_cost_num FROM invoices WHERE num = %s"
        self.__update_query = "UPDATE invoices SET date_departure = %(date_departure)s, " \
                              "date_arrival = %(date_arrival)s, shipping_cost = %(shipping_cost)s, " \
                              "sender_ipn = %(sender_ipn)s, recipient_ipn = %(recipient_ipn)s, " \
                              "warehouse_dep_num = %(warehouse_dep_num)s, warehouse_arr_num = %(warehouse_arr_num)s " \
                              "WHERE num = %(num)s"
        self.__delete_query = "DELETE FROM invoices WHERE num = %s"
        self.__select_with_join_query = ""
        self.__select_many_query = "SELECT *, shipping_cost::numeric as shipping_cost_num FROM invoices " \
                                   "ORDER BY num OFFSET %(offset)s LIMIT %(limit)s"
        self.__select_many_with_join_query = ""
        self.__count_query = "SELECT COUNT(*) FROM invoices"

    def create(self, inv: Invoice):
        self._cursor.execute(self.__insert_query, inv.__dict__)
        self._connection.commit()
        row = self._cursor.fetchone()
        if row is not None and isinstance(row['num'], int):
            inv.num = row['num']
            return inv
        else:
            raise Exception("No rows received from DB")

    def create_many(self, items: [Invoice], get_ids: bool = False):
        if get_ids:
            for item in items:
                self.create(item)
            return items
        else:
            self._cursor.executemany(self.__insert_query, [item.__dict__ for item in items])
            self._connection.commit()

    def read(self, num: int):
        self._cursor.execute(self.__select_query, [num])
        row = self._cursor.fetchone()
        if self.__is_row_invoice(row):
            return self.__get_invoice_from_row(row)
        else:
            raise Exception("No rows received from DB")

    def read_all(self, offset: int, limit: int = None):
        self._cursor.execute(self.__select_many_query, {'limit': limit, 'offset': offset})
        rows = self._cursor.fetchall()
        if isinstance(rows, list) and all([self.__is_row_invoice(row) for row in rows]):
            return [self.__get_invoice_from_row(row) for row in rows]
        else:
            raise Exception("No rows received from DB")

    def count_all(self):
        self._cursor.execute(self.__count_query)
        row = self._cursor.fetchone()
        if row is not None and isinstance(row['count'], int):
            return row['count']
        else:
            raise Exception("No rows received from DB")

    def update(self, inv: Invoice):
        if not isinstance(inv.num, int):
            raise Exception("No num of invoice provided")
        self._cursor.execute(self.__update_query, inv.__dict__)
        self._connection.commit()

    def delete(self, num: int):
        if not isinstance(num, int):
            raise Exception("No num of invoice provided")
        self._cursor.execute(self.__delete_query, [num])
        self._connection.commit()

    @staticmethod
    def __is_row_invoice(row):
        return row is not None \
               and [isinstance(row[column], int) for column in ['sender_ipn', 'recipient_ipn', 'warehouse_dep_num',
                                                                'warehouse_arr_num', 'num']] \
               and isinstance(row['date_arrival'], (type(None), date)) and isinstance(row['date_departure'], date) \
               and isinstance(row['shipping_cost_num'], Decimal)

    @staticmethod
    def __get_invoice_from_row(row):
        return Invoice(row['date_departure'], row['shipping_cost_num'], row['sender_ipn'], row['recipient_ipn'],
                       row['warehouse_dep_num'], row['warehouse_arr_num'], row['date_arrival'], row['num'])
