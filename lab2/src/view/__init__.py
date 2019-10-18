from abc import ABC, abstractmethod
from settings import MessageType
from math import ceil


class BaseView(ABC):
    def __init__(self, name, common_view):
        self.__name = name
        self.__common_view = common_view

    def show_message(self, msg: str, msg_type: MessageType):
        return self.__common_view.draw_text(msg, msg_type)

    def show_operations(self, list_operations: [str]):
        return self.__common_view.draw_menu(list_operations, self.__name)

    def show_items_table(self, items: [object], count_all: int, primary_key_name: str, offset: int = 0, limit: int = None):
        table_head = self._items_table_header()
        heading = f'{self.__name.upper()} LIST'

        if limit is not None and limit > 0:
            list_page_status = f'Listed {len(items)} of {count_all}. Page {offset // limit + 1} of {ceil(count_all / limit):d}'
        else:
            list_page_status = 'Listed all items'
        return self.__common_view.draw_list([{'id': getattr(item, primary_key_name), 'str': self._table_row_from_item(item)} for item in items], heading,
                                            table_head, list_page_status)

    def show_create_item_form(self, input_items: [dict]):
        return self.__common_view.draw_input(input_items, f'Create {self.__name}')

    def show_modal_question(self, prompt: str, state_name: str):
        return self.__common_view.draw_modal_prompt(prompt, )

    @staticmethod
    @abstractmethod
    def show_item(item: object):
        pass

    @staticmethod
    @abstractmethod
    def _items_table_header():
        pass

    @staticmethod
    @abstractmethod
    def _table_row_from_item(item: object):
        pass
