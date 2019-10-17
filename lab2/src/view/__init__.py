from abc import ABC, abstractmethod
from settings import MessageType
from math import ceil


class BaseView(ABC):
    def __init__(self, name, common_view):
        self.__name = name
        self.__common_view = common_view

    def show_message(self, msg: str, msg_type: MessageType):
        self.__common_view.draw_text(msg, msg_type)

    def show_operations(self, list_operations: [str]):
        return self.__common_view.draw_menu(list_operations, self.__name)

    def show_items_table(self, items: [object], count_all: int, primary_key_name: str, offset: int = 0, limit: int = None):
        table_head = self._table_head()
        heading = f'{self.__name.upper()} LIST'

        if limit is not None and limit > 0:
            list_page_status = f'Listed {len(items)} of {count_all}. Page {offset // limit + 1} of {ceil(count_all / limit):d}'
        else:
            list_page_status = 'Listed all items'
        return self.__common_view.draw_list([{'id': getattr(item, primary_key_name), 'str': self._item_as_row(item)} for item in items], heading,
                                            table_head, list_page_status)

    def show_create_item_form(self, input_items: [dict]):
        return self.__common_view.draw_input(input_items, f'Create {self.__name}')

    #
    # @staticmethod
    # def display_missing_item_error(item, err):
    #     print('**************************************************************')
    #     print('We are sorry, we have no {}!'.format(item.upper()))
    #     print('{}'.format(err.args[0]))
    #     print('**************************************************************')
    #
    # @staticmethod
    # def display_item_already_stored_error(item, item_type, err):
    #     print('**************************************************************')
    #     print('Hey! We already have {} in our {} list!'
    #           .format(item.upper(), item_type))
    #     print('{}'.format(err.args[0]))
    #     print('**************************************************************')
    #
    # @staticmethod
    # def display_item_not_yet_stored_error(item, item_type, err):
    #     print('**************************************************************')
    #     print('We don\'t have any {} in our {} list. Please insert it first!'
    #           .format(item.upper(), item_type))
    #     print('{}'.format(err.args[0]))
    #     print('**************************************************************')
    #
    # @staticmethod
    # def display_item_stored(item, item_type):
    #     print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #     print('Hooray! We have just added some {} to our {} list!'
    #           .format(item.upper(), item_type))
    #     print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #
    # @staticmethod
    # def display_change_item_type(older, newer):
    #     print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
    #     print('Change item type from "{}" to "{}"'.format(older, newer))
    #     print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
    #
    # @staticmethod
    # def display_item_updated(item, o_price, o_quantity, n_price, n_quantity):
    #     print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
    #     print('Change {} price: {} --> {}'
    #           .format(item, o_price, n_price))
    #     print('Change {} quantity: {} --> {}'
    #           .format(item, o_quantity, n_quantity))
    #     print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
    #
    # @staticmethod
    # def display_item_deletion(name):
    #     print('--------------------------------------------------------------')
    #     print('We have just removed {} from our list'.format(name))
    #     print('--------------------------------------------------------------')

    @staticmethod
    @abstractmethod
    def show_item(item: object):
        pass

    @staticmethod
    @abstractmethod
    def _table_head():
        pass

    @staticmethod
    @abstractmethod
    def _item_as_row(item: object):
        pass

    @staticmethod
    def __table_heading(heading: str, table_length: int, heading_length: int):
        if heading_length >= table_length:
            return heading
        else:
            border = '-' * ((table_length - heading_length // 2) - 1)
            return f'{border} {heading} {border}'
