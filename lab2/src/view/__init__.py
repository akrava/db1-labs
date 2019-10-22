from abc import ABC, abstractmethod
from settings import MessageType
from math import ceil


class BaseView(ABC):
    def __init__(self, name, common_view):
        self.__name = name
        self.__common_view = common_view

    def show_error(self, msg: str):
        return self.__common_view.draw_text(msg, MessageType.ERROR)

    def show_success(self, msg: str):
        return self.__common_view.draw_text(msg, MessageType.SUCCESSFUL)

    def show_operations(self, list_operations: [str]):
        return self.__common_view.draw_menu(list_operations, self.__name)

    def show_item(self, item: object):
        return self.__common_view.draw_text(self._item_to_text(item), MessageType.INFO)

    def show_items_table(self, items: [object], primary_key_name: str,
                         count_all: int, offset: int, limit: int):
        table_head = self._items_table_header()
        heading = f'{self.__name.upper()} LIST'
        list_page_status = f'Listed {len(items)} of {count_all}. ' \
                           f'Page {offset // limit + 1} of {ceil(count_all / limit):d}' \
            if count_all > 0 else 'There are no items here'
        items_list = [{'id': getattr(item, primary_key_name),
                       'str': self._table_row_from_item(item)} for item in items]
        return self.__common_view.draw_list(items_list, heading, table_head, list_page_status)

    def get_item_pk(self, purpose: str):
        question = f'Enter unique identifier of {self.__name}:'
        return self.__common_view.draw_modal_prompt(question, f'{purpose} {self.__name} item')

    def show_input_item_form(self, input_items: [dict], purpose: str):
        return self.__common_view.draw_input(input_items, f'{purpose} {self.__name}')

    def show_created_item(self, item: object, pk_name: str):
        message = f'Item was successfully created.'
        if item is not None:
            message += f" {pk_name}: {getattr(item, pk_name)}\n{item}"
        return self.show_success(message)

    def show_updated_item(self, before: object, after: object):
        message = f'Item was successfully updated.\n\nBefore update:\n{before}\n\nAfter:\n{after}'
        return self.show_success(message)

    def confirm_deleting_form(self, item: object):
        question = f'Enter YES to delete {item}'
        return self.__common_view.draw_modal_prompt(question, f'Deleting {self.__name} item')

    @staticmethod
    @abstractmethod
    def _item_to_text(item: object):
        pass

    @staticmethod
    @abstractmethod
    def _items_table_header():
        pass

    @staticmethod
    @abstractmethod
    def _table_row_from_item(item: object):
        pass
