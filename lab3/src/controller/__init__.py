from typing import Callable, Tuple, Optional, Type
from settings import ConsoleCommands
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from view import BaseView
from model import Model


class BaseController(ABC):
    def __init__(self, session: Session, cls: Type, view: BaseView):
        self.__model = Model(session, cls)
        self.__cls = cls
        self._view = view
        self._cb_show_prev_state = None

    @property
    def model(self):
        return self.__model

    def show(self, pk: int = None):
        pk_not_specified = pk is None
        if pk_not_specified:
            pk = self._view.get_item_pk('Reading')
        try:
            if isinstance(pk, str):
                pk = int(pk)
            item = self.__model.read(pk)
            self._view.show_item(item)
        except Exception as e:
            self._view.show_error(str(e))
        finally:
            if pk_not_specified:
                self.choose_operation()
            else:
                self.show_all()

    def show_all(self):
        limit = 15
        offset = 0
        try:
            while True:
                items = self.__model.read_all(offset, limit)
                count_all = self.__model.count_all()
                command = self._view.show_items_table(items, self.__model.get_primary_key_name(),
                                                      count_all, offset, limit)
                if command == ConsoleCommands.PREV_PAGE:
                    if offset >= limit:
                        offset -= limit
                elif command == ConsoleCommands.NEXT_PAGE:
                    if offset + limit < count_all:
                        offset += limit
                elif command == ConsoleCommands.GO_BACK:
                    return self.choose_operation()
                elif command is not None:
                    return self.show(command)
                else:
                    break
        except Exception as e:
            self._view.show_error(str(e))
        finally:
            self.choose_operation()

    def insert(self):
        input_items = self.__get_input_items_form(self._prompt_values_for_input())
        command = self._view.show_input_item_form(input_items, 'Create')
        if command == ConsoleCommands.GO_BACK:
            return self.choose_operation()
        if command == ConsoleCommands.CONFIRM:
            try:
                pk_name = self.__model.get_primary_key_name()
                item = self.__model.create(self.__create_instance_from_input(input_items))
                self._view.show_created_item(item, pk_name)
            except Exception as e:
                self._view.show_error(str(e))
            finally:
                self.choose_operation()

    def update(self):
        pk = self._view.get_item_pk('Updating')
        try:
            if isinstance(pk, str):
                pk = int(pk)
            item = self.__model.read(pk)
            item_before_str = item.__str__()
            input_items = self.__get_input_items_form(self._prompt_values_for_input(item, True))
            command = self._view.show_input_item_form(input_items, 'Update')
            if command == ConsoleCommands.GO_BACK:
                return self.choose_operation()
            if command == ConsoleCommands.CONFIRM:
                new_item_dict = self._create_dict_from_input(input_items)
                pk_name = self.__model.get_primary_key_name()
                new_item_dict[pk_name] = getattr(item, pk_name)
                new_item = self.__model.update(new_item_dict)
                self._view.show_updated_item(item_before_str, new_item)
        except Exception as e:
            self._view.show_error(str(e))
        finally:
            self.choose_operation()

    def delete(self):
        pk = self._view.get_item_pk('Deleting')
        try:
            if isinstance(pk, str):
                pk = int(pk)
            item = self.__model.read(pk)
            confirm = self._view.confirm_deleting_form(item)
            if confirm.strip().lower() != "yes":
                return self.choose_operation()
            self.__model.delete(pk)
            self._view.show_success(f"An item {item} was successfully deleted")
        except Exception as e:
            self._view.show_error(str(e))
        finally:
            self.choose_operation()

    def choose_operation(self, previous_state: Callable = None):
        if previous_state is not None:
            self._cb_show_prev_state = previous_state
        list_operations = ['Create', 'Read', 'Update', 'Delete', 'List all']
        operation = self._view.show_operations(list_operations)
        if operation == 0:
            self.insert()
        elif operation == 1:
            self.show()
        elif operation == 2:
            self.update()
        elif operation == 3:
            self.delete()
        elif operation == 4:
            self.show_all()
        elif operation == ConsoleCommands.GO_BACK:
            self._cb_show_prev_state()

    @staticmethod
    def __get_input_items_form(tup: Tuple[list, Optional[list]]):
        if tup[1] is None:
            return [{'name': name, 'value': None} for name in tup[0]]
        return [{'name': name, 'value': val} for name, val in zip(tup[0], tup[1])]

    @staticmethod
    @abstractmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        pass

    @staticmethod
    @abstractmethod
    def _create_dict_from_input(input_items: [dict]):
        pass

    def __create_instance_from_input(self, input_items: [dict]):
        return self.__cls(**self._create_dict_from_input(input_items))
