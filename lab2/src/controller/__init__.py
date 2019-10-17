from abc import ABC, abstractmethod
from settings import ConsoleCommands, MessageType
from typing import Callable
from model import BaseModel
from view import BaseView
import psycopg2


class BaseController(ABC):
    def __init__(self, model: BaseModel, view: BaseView):
        self.__model = model
        self.__view = view
        self._cb_show_prev_state = None

    def show(self, pk: int = None):
        if pk is None:
            pass
        try:
            item = self.__model.read(pk)
        except (Exception, psycopg2.Error) as e:
            self.__view.show_message(str(e), MessageType.ERROR)
            self.choose_operation()

    def show_all(self):
        limit = 15
        offset = 0
        try:
            while True:
                items = self.__model.read_all(offset, limit)
                count_all = self.__model.count_all()
                command = self.__view.show_items_table(items, count_all, self.__model.primary_key_name, offset, limit)
                if command == ConsoleCommands.PREV_PAGE:
                    if offset >= limit:
                        offset -= limit
                elif command == ConsoleCommands.NEXT_PAGE:
                    if offset + limit < count_all:
                        offset += limit
                elif command == ConsoleCommands.GO_BACK:
                    return self.choose_operation()
                else:
                    break
        except (Exception, psycopg2.Error) as e:
            self.__view.show_message(str(e), MessageType.ERROR)
            self.choose_operation()

    def insert(self):
        input_items = [{'name': item, 'value': None} for item in self._prompt_for_item_attributes()]
        command = self.__view.show_create_item_form(input_items)
        if command == 0:
            return self.choose_operation()
        if command == 1:
            try:
                self.__model.create(self._create_obj_from_input(input_items))
                self.__view.show_message("Yee", MessageType.SUCCESSFUL)
            except (Exception, psycopg2.Error) as e:
                self.__view.show_message(str(e), MessageType.ERROR)
            finally:
                self.choose_operation()
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

    def choose_operation(self, previous_state: Callable = None):
        if previous_state is not None:
            self._cb_show_prev_state = previous_state
        list_operations = ['Create', 'Read', 'Update', 'Delete', 'List all']
        operation = self.__view.show_operations(list_operations)
        if operation == 0:
            self.insert()
        elif operation == 1:
            pass
        elif operation == 2:
            pass
        elif operation == 3:
            pass
        elif operation == 4:
            self.show_all()
        elif operation == 5:
            self._cb_show_prev_state()

    @staticmethod
    @abstractmethod
    def _prompt_for_item_attributes():
        pass

    @staticmethod
    @abstractmethod
    def _create_obj_from_input(input_items: [dict]):
        pass
