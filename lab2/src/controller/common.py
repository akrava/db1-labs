from controller.city import CityController
from controller.contragent import ContragentController
from controller.goods import GoodsController
from controller.invoice import InvoiceController
from controller.werehouse import WarehouseController
from model.common import Model
from view.common import View
import psycopg2
import logging


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
        elif menu_option == 5:
            self.start()

    def batch_generation_data(self):
        pass

    def search_multiple_attr(self):
        pass

    def fulltext_search(self):
        pass

    def service_operations(self):
        pass
