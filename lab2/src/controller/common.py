from settings import ConsoleCommands, MessageType, exception_handler
from controller.contragent import ContragentController, Contragent
from controller.werehouse import WarehouseController, Warehouse
from controller.invoice import InvoiceController, Invoice
from controller.goods import GoodsController, Goods
from controller.city import CityController, City
from model.common import Model
from view.common import View
from typing import Callable
from datetime import date
import urllib.request
import psycopg2
import decimal
import logging
import random
import json


class Controller:
    def __init__(self, connection, program_name):
        self.__common_view = View(program_name)
        self.__common_model = Model(connection)
        self.__city_controller = CityController(connection, self.__common_view)
        self.__contragent_controller = ContragentController(connection, self.__common_view)
        self.__goods_controller = GoodsController(connection, self.__common_view)
        self.__invoice_controller = InvoiceController(connection, self.__common_view)
        self.__warehouse_controller = WarehouseController(connection, self.__common_view)

    def start(self):
        try:
            self.__common_model.create_tables()
            logging.info("Successfully created tables in DB if they did not exist")
        except (Exception, psycopg2.Error) as e:
            exception_handler(e, self.__common_model.rollback)
            logging.exception(e)
            print("Couldn't init tables in DB. Exiting...")
            exit(1)
        self.__common_view.start_app()
        list_menu = ['CRUD operations with relations', 'Batch generation of "randomized" data',
                     'Search by multiple attributes of two entities', 'Full text search',
                     'Service operations with DB']
        menu_option = self.__common_view.draw_menu(list_menu, 'Main menu', True)
        if menu_option == 0:
            self.crud_operations()
        elif menu_option == 1:
            self.batch_generation_data()
        elif menu_option == 2:
            self.search_multiple_attr()
        elif menu_option == 3:
            self.fulltext_search()
        elif menu_option == 4:
            self.service_operations()

    def crud_operations(self):
        list_menu = ['Contragents', 'Cities', 'Warehouses', 'Invoices', 'Goods']
        menu_option = self.__common_view.draw_menu(list_menu, 'CRUD operations with relations')
        if menu_option == 0:
            self.__contragent_controller.choose_operation(self.crud_operations)
        elif menu_option == 1:
            self.__city_controller.choose_operation(self.crud_operations)
        elif menu_option == 2:
            self.__warehouse_controller.choose_operation(self.crud_operations)
        elif menu_option == 3:
            self.__invoice_controller.choose_operation(self.crud_operations)
        elif menu_option == 4:
            self.__goods_controller.choose_operation(self.crud_operations)
        elif menu_option == ConsoleCommands.GO_BACK:
            self.start()

    def batch_generation_data(self):
        try:
            action_name = 'Batch generation of "randomized" data'
            num_str = self.__common_view.draw_modal_prompt('Enter n > 2 - amount of items to generate:', action_name)
            n = int(num_str)
            if n < 3:
                raise Exception(f'n should be > 0, got {n}')
            cities = self.__random_cities(n)
            self.__city_controller.model.create_many(cities, True)
            contragents = self.__random_contragents(n)
            self.__contragent_controller.model.create_many(contragents, True)
            warehouses = self.__random_warehouses(cities, n)
            self.__warehouse_controller.model.create_many(warehouses, True)
            invoices = self.__random_invoices(contragents, warehouses, n)
            self.__invoice_controller.model.create_many(invoices, True)
            goods = self.__random_goods(invoices, min(n, 10))
            self.__goods_controller.model.create_many(goods, True)
            self.__common_view.draw_text(f"Successfully generated data! Amounts:\n"
                                         f"Cities: {len(cities)}\n"
                                         f"Contragents: {len(contragents)}\n"
                                         f"Warehouses: {len(warehouses)}\n"
                                         f"Invoices: {len(invoices)}\n"
                                         f"Goods: {len(goods)}", MessageType.SUCCESSFUL)
        except (Exception, psycopg2.Error) as e:
            exception_handler(e, self.__common_model.rollback)
            self.__common_view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.start()

    def search_multiple_attr(self):
        try:
            min_cost, max_cost = self.__invoice_controller.model.get_extremum_shipping_cost()
            names = self.__contragent_controller.model.get_distinct_names()
            names.insert(0, "<any>")
            command = self.__common_view.draw_filtering(min_cost, max_cost, names, 0, 0)
            if command == ConsoleCommands.GO_BACK:
                return self.start()
            sender_i = names[command['sender_i']] if names[command['sender_i']] != "<any>" else None
            recipient_i = names[command['recipient_i']] if names[command['recipient_i']] != "<any>" else None
            results = self.__common_model.filter_items(command['min'], command['max'], sender_i, recipient_i)
            self.__common_view.draw_text(str(results))
        except (Exception, psycopg2.Error) as e:
            exception_handler(e, self.__common_model.rollback)
            self.__common_view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.start()

    def fulltext_search(self):
        list_menu = ['The word is not included', 'Required word occurrence']
        menu_option = self.__common_view.draw_menu(list_menu, 'Full text search')
        if menu_option == 0:
            self.fulltext_search_excluded()
        elif menu_option == 1:
            self.fulltext_search_included()
        elif menu_option == ConsoleCommands.GO_BACK:
            self.start()

    def fulltext_search_excluded(self):
        try:
            command = self.__common_view.draw_modal_prompt('Enter query:', 'Fulltext search excluding words')
            res = self.__common_model.fulltext_search(command, False)
            self.__common_view.draw_text(str(res))
        except (Exception, psycopg2.Error) as e:
            exception_handler(e, self.__common_model.rollback)
            self.__common_view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.fulltext_search()

    def fulltext_search_included(self):
        try:
            command = self.__common_view.draw_modal_prompt('Enter query:', 'Fulltext search including words')
            res = self.__common_model.fulltext_search(command, True)
            self.__common_view.draw_text(str(res))
        except (Exception, psycopg2.Error) as e:
            exception_handler(e, self.__common_model.rollback)
            self.__common_view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.fulltext_search()

    def service_operations(self):
        list_menu = ['Create tables', 'Truncate tables', 'Drop tables']
        menu_option = self.__common_view.draw_menu(list_menu, 'Service operations with DB')
        if menu_option == 0:
            self.create_tables()
        elif menu_option == 1:
            self.truncate_tables()
        elif menu_option == 2:
            self.drop_tables()
        elif menu_option == ConsoleCommands.GO_BACK:
            self.start()

    def create_tables(self):
        try:
            self.__common_model.create_tables()
            self.__common_view.draw_text("Successfully created tables if not exists", MessageType.SUCCESSFUL)
        except (Exception, psycopg2.Error) as e:
            exception_handler(e, self.__common_model.rollback)
            self.__common_view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.service_operations()

    def truncate_tables(self):
        self.__perform_risky_action('truncate tables', 'Truncating tables',
                                    self.__common_model.truncate_tables,
                                    'truncated tables')

    def drop_tables(self):
        self.__perform_risky_action('drop tables', 'Dropping tables',
                                    self.__common_model.truncate_tables,
                                    'dropped tables')

    def __perform_risky_action(self, purpose: str, action_name: str, action_cb: Callable, success: str):
        try:
            command = self.__common_view.draw_modal_prompt(f'Enter YES to {purpose}', action_name)
            if command.strip().lower() == "yes":
                action_cb()
                self.__common_view.draw_text(f"Successfully {success}", MessageType.SUCCESSFUL)
        except (Exception, psycopg2.Error) as e:
            exception_handler(e, self.__common_model.rollback)
            self.__common_view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.service_operations()

    # Methods for random generation items

    @staticmethod
    def __random_cities(amount: int = 1):
        return [City(name) for name in Controller.__random_city_name(amount)]

    @staticmethod
    def __random_contragents(amount: int = 1):
        names = Controller.__random_name(amount)
        phone_numbers = Controller.__random_phone_number(amount)
        ipn_set = set()
        counter = 0
        while counter < amount:
            val = random.randint(1000000, 9999999)
            if val not in ipn_set:
                ipn_set.add(val)
                counter += 1
        return [Contragent(ipn, name, phone_number) for name, phone_number, ipn
                in zip(names, phone_numbers, ipn_set)]

    @staticmethod
    def __random_warehouses(cities: [City], amount: int = 1):
        phone_numbers = Controller.__random_phone_number(amount)
        addresses = Controller.__random_address(amount)
        city_ids = []
        counter = 0
        while counter < amount:
            city_ids.append(Controller.__get_random_element(cities).id)
            counter += 1
        return [Warehouse(address, phone_number, city_id) for address, phone_number, city_id
                in zip(addresses, phone_numbers, city_ids)]

    @staticmethod
    def __random_invoices(contragents: [Contragent], warehouses: [Warehouse], amount: int = 1):
        dates_dep, dates_arr = Controller.__random_dates_intervals(amount)
        shipping_costs = [decimal.Decimal(random.randint(5000 + i, 150000 + i))/100 for i in range(amount)]
        senders_ipn = []
        recipients_ipn = []
        warehouse_dep_nums = []
        warehouse_arr_nums = []
        counter = 0
        while counter < amount:
            Controller.__append_uniq_elements(senders_ipn, recipients_ipn, contragents, 'ipn')
            Controller.__append_uniq_elements(warehouse_dep_nums, warehouse_arr_nums, warehouses, 'num')
            counter += 1
        return [Invoice(date_dep, cost, send_ipn, recp_ipn, war_dep_num, war_arr_num, date_arr)
                for date_dep, date_arr, cost, send_ipn, recp_ipn, war_dep_num, war_arr_num
                in zip(dates_dep, dates_arr, shipping_costs, senders_ipn, recipients_ipn,
                       warehouse_dep_nums, warehouse_arr_nums)]

    @staticmethod
    def __random_goods(invoices: [Invoice], amount_per_invoice: int = 1):
        invoices_id = []
        for invoice in invoices:
            counter = 0
            while counter < amount_per_invoice:
                invoices_id.append(invoice.num)
                if random.randrange(20) % 4 == 1:
                    break
                counter += 1
        amount = len(invoices_id)
        heights = [random.randint(100 + i, 10000 + i) for i in range(amount)]
        widths = [random.randint(100 + i, 10000 + i) for i in range(amount)]
        depths = [random.randint(100 + i, 10000 + i) for i in range(amount)]
        weights = [random.randint(100 + i, 1000000 + i) for i in range(amount)]
        descriptions = Controller.__random_description(amount, True)
        return [Goods(height, width, depth, weight, inv_id, description)
                for height, width, depth, weight, description, inv_id
                in zip(heights, widths, depths, weights, descriptions, invoices_id)]

    @staticmethod
    def __random_name(amount: int = 1):
        url = f"https://randomuser.me/api/?inc=name&nat=gb&results={amount}&noinfo"
        content = Controller.__get_content(url)
        names = []
        for item in content['results']:
            name = item['name']
            names.append(f"{name['first']} {name['last']}")
        return names

    @staticmethod
    def __random_phone_number(amount: int = 1):
        url = f"https://randomuser.me/api/?inc=phone&nat=us&results={amount}&noinfo"
        content = Controller.__get_content(url)
        phone_numbers = []
        for item in content['results']:
            phone_numbers.append(item['phone'])
        return phone_numbers

    @staticmethod
    def __random_city_name(amount: int = 1):
        url = f"https://randomuser.me/api/?inc=location&nat=gb&results={amount}&noinfo"
        content = Controller.__get_content(url)
        cities = []
        for item in content['results']:
            location = item['location']
            cities.append(location['city'])
        return cities

    @staticmethod
    def __random_address(amount: int = 1):
        url = f"https://randomuser.me/api/?inc=location&nat=gb&results={amount}&noinfo"
        content = Controller.__get_content(url)
        address = []
        for item in content['results']:
            street = item['location']['street']
            address.append(f"{street['name']}, {street['number']}")
        return address

    @staticmethod
    def __random_description(amount: int = 1, enable_none: bool = False):
        url = f"https://makemeapassword.ligos.net/api/v1/passphrase/json"
        descriptions = []
        count = 0
        while count < amount:
            if enable_none and random.randrange(10) % 4 == 1:
                descriptions.append(None)
            else:
                content = Controller.__get_content(url)
                descriptions.append(content['pws'][0])
            count += 1
        return descriptions

    @staticmethod
    def __random_dates_intervals(amount: int = 1):
        dates_start = []
        dates_end = []
        counter = 0
        while counter < amount:
            start_dt = date.today().replace(day=1, month=1).toordinal()
            end_dt = date.today().toordinal()
            random_day = date.fromordinal(random.randint(start_dt, end_dt))
            dates_start.append(random_day)
            if random.randrange(10) % 4 != 1:
                start_dt = date.today().toordinal()
                end_dt = date.today().replace(day=31, month=12).toordinal()
                random_day = date.fromordinal(random.randint(start_dt, end_dt))
                dates_end.append(random_day)
            else:
                dates_end.append(None)
            counter += 1
        return dates_start, dates_end

    @staticmethod
    def __get_random_element(elements: list):
        return elements[random.randint(0, len(elements) - 1)]

    @staticmethod
    def __append_uniq_elements(first: list, second: list, source: list, attr: str):
        first.append(getattr(Controller.__get_random_element(source), attr))
        another = first[len(first) - 1]
        while another == first[len(first) - 1]:
            another = getattr(Controller.__get_random_element(source), attr)
        second.append(another)

    @staticmethod
    def __get_content(url: str):
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        return json.loads(r.decode('utf-8'))
