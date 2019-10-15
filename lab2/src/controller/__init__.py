from abc import ABC, abstractmethod
from typing import Callable
from model import BaseModel
from view import BaseView
import psycopg2
import sys


class BaseController(ABC):
    def __init__(self, model: BaseModel, view: BaseView):
        self.__model = model
        self.__view = view

    # def show(self, bullet_points=False):
    #     items = self.model.read_items()
    #     item_type = self.model.item_type
    #     if bullet_points:
    #         self.view.show_bullet_point_list(item_type, items)
    #     else:
    #         self.view.show_number_point_list(item_type, items)

    def show_all(self):
        limit = 10
        offset = 0
        try:
            items = self.__model.read_all(offset, limit)
            count_all = self.__model.count_all()
            while True:
                command = self.__view.show_items_table(items, count_all, offset, limit)
                if command == sys.maxsize - 1:
                    pass
                elif command == sys.maxsize:
                    pass
                else:
                    break
        except (Exception, psycopg2.Error) as e:
            print(e)
        pass

    # def insert(self, name, price, quantity):
    #     assert price > 0, 'price must be greater than 0'
    #     assert quantity >= 0, 'quantity must be greater than or equal to 0'
    #     item_type = self.model.item_type
    #     try:
    #         self.model.create_item(name, price, quantity)
    #         self.view.display_item_stored(name, item_type)
    #     except mvc_exc.ItemAlreadyStored as e:
    #         self.view.display_item_already_stored_error(name, item_type, e)
    #
    # def insert_many(self, name, price, quantity):
    #     assert price > 0, 'price must be greater than 0'
    #     assert quantity >= 0, 'quantity must be greater than or equal to 0'
    #     item_type = self.model.item_type
    #     try:
    #         self.model.create_item(name, price, quantity)
    #         self.view.display_item_stored(name, item_type)
    #     except mvc_exc.ItemAlreadyStored as e:
    #         self.view.display_item_already_stored_error(name, item_type, e)
    #
    # def update(self, name, price, quantity):
    #     assert price > 0, 'price must be greater than 0'
    #     assert quantity >= 0, 'quantity must be greater than or equal to 0'
    #     item_type = self.model.item_type
    #
    #     try:
    #         older = self.model.read_item(name)
    #         self.model.update_item(name, price, quantity)
    #         self.view.display_item_updated(
    #             name, older['price'], older['quantity'], price, quantity)
    #     except mvc_exc.ItemNotStored as e:
    #         self.view.display_item_not_yet_stored_error(name, item_type, e)
    #         # if the item is not yet stored and we performed an update, we have
    #         # 2 options: do nothing or call insert_item to add it.
    #         # self.insert_item(name, price, quantity)
    #
    # def delete(self, name):
    #     item_type = self.model.item_type
    #     try:
    #         self.model.delete_item(name)
    #         self.view.display_item_deletion(name)
    #     except mvc_exc.ItemNotStored as e:
    #         self.view.display_item_not_yet_stored_error(name, item_type, e)

    def choose_operation(self, previous_state: Callable):
        list_operations = ['Create', 'Read', 'Update', 'Delete', 'List all']
        operation = self.__view.show_operations(list_operations)
        if operation == 0:
            pass
        elif operation == 1:
            pass
        elif operation == 2:
            pass
        elif operation == 3:
            pass
        elif operation == 4:
            self.show_all()
        elif operation == 5:
            previous_state()
