from settings import ConsoleCommands, MessageType
from typing import Callable
from decimal import Decimal
import textwrap
import curses
import sys


class View:
    def __init__(self, program_name):
        self.__name = program_name
        self.__std_scr = None
        self.__width = None
        self.__height = None
        self.__state = []
        self.__prev_index = 0
        self.__should_exit = False

    def __del__(self):
        if self.__std_scr is not None:
            curses.curs_set(1)
            curses.nocbreak()
            self.__std_scr.keypad(0)
            curses.echo()
            curses.endwin()

    def start_app(self):
        self.__std_scr = curses.initscr()
        self.__height, self.__width = self.__std_scr.getmaxyx()
        if self.__height < 24 or self.__width < 80:
            print("Terminal sizes should be >= 24x80. Restart app with proper sizes")
            exit(1)
        curses.noecho()
        curses.cbreak()
        self.__std_scr.keypad(1)
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)
        curses.init_pair(6, curses.COLOR_RED, -1)
        curses.init_pair(7, curses.COLOR_MAGENTA, -1)

    def draw_list(self, items_list: [dict], state_name: str, table_heading: str, list_page_status: str):
        current_index = self.__prev_index if 0 <= self.__prev_index < len(items_list) else 0

        def __draw_list_instance(key: int):
            nonlocal current_index
            current_index = self.__calculate_current_index(key, current_index, len(items_list) - 1)
            self.__draw_subtitle(state_name)
            self.__std_scr.addstr(4, 0, table_heading)
            self.__std_scr.addstr(5, 0, '-' * len(table_heading))
            self.__std_scr.addstr(self.__height - 2, 0, list_page_status, curses.color_pair(5))
            y_pos = 6
            for (i, item) in enumerate(items_list):
                if i == current_index:
                    self.__std_scr.addstr(y_pos + i, 0, item['str'], curses.color_pair(2) | curses.A_BOLD)
                else:
                    self.__std_scr.addstr(y_pos + i, 0, item['str'])
            self.__std_scr.addstr(y_pos + len(items_list), 0, '-' * len(table_heading))
            if key == curses.KEY_ENTER or key == ord('\n'):
                self.__state.append(current_index)
                self.__prev_index = 0
                return items_list[current_index]['id']
            elif key == curses.KEY_BACKSPACE:
                self.__prev_index = self.__state.pop()
                return ConsoleCommands.GO_BACK
            elif key == curses.KEY_LEFT:
                return ConsoleCommands.PREV_PAGE
            elif key == curses.KEY_RIGHT:
                return ConsoleCommands.NEXT_PAGE
            else:
                return ConsoleCommands.STANDBY
        return self.draw_app(__draw_list_instance)

    def draw_menu(self, items_list: [str], state_name: str, is_root_menu: bool = False):
        current_index = self.__prev_index if 0 <= self.__prev_index < len(items_list) else 0

        def __draw_menu_instance(key: int):
            nonlocal current_index
            current_index = self.__calculate_current_index(key, current_index, len(items_list) - 1)
            self.__draw_subtitle(state_name)
            y_pos = 4
            for (i, item) in enumerate(items_list):
                if i == current_index:
                    self.__std_scr.addstr(y_pos + i, 0, f'-> {item}', curses.color_pair(2) | curses.A_BOLD)
                else:
                    self.__std_scr.addstr(y_pos + i, 0, f' * {item}')
            if key == curses.KEY_ENTER or key == ord('\n'):
                self.__state.append(current_index)
                self.__prev_index = 0
                return current_index
            elif key == curses.KEY_BACKSPACE and not is_root_menu:
                self.__prev_index = self.__state.pop()
                return ConsoleCommands.GO_BACK
            else:
                return ConsoleCommands.STANDBY
        return self.draw_app(__draw_menu_instance)

    def draw_text(self, message: str, type_msg: MessageType = MessageType.INFO):
        def __draw_text_instance(key: int):
            self.__draw_subtitle(type_msg.name)
            color_text_palette = 0
            if type_msg == MessageType.ERROR:
                color_text_palette = curses.color_pair(6)
            elif type_msg == MessageType.SUCCESSFUL:
                color_text_palette = curses.color_pair(2)
            self.__std_scr.addstr(4, 0, message, color_text_palette)
            self.__std_scr.addstr(self.__height - 1, 0, ' ' * (self.__width - 1), curses.color_pair(3))
            status_bar = "Press 'q' to exit | Press any key to go back"
            self.__std_scr.addstr(self.__height - 1, 0, status_bar, curses.color_pair(3))
            if key != 0:
                self.__prev_index = self.__state.pop()
            return ConsoleCommands.GO_BACK if key != 0 else ConsoleCommands.STANDBY
        return self.draw_app(__draw_text_instance)

    def draw_modal_prompt(self, prompt: str, state_name: str):
        def __draw_modal_prompt(key: int):
            self.__draw_subtitle(state_name)
            length = 40
            text_lines = textwrap.wrap(prompt, length)
            y_offset = (self.__height - len(text_lines)) // 2
            x_offset = (self.__width - length) // 2
            for line in text_lines:
                self.__std_scr.addstr(y_offset, x_offset, line, curses.color_pair(7) | curses.A_BOLD)
                y_offset += 1
            status_bar = "Input specified data and press Enter"
            self.__std_scr.addstr(self.__height - 1, 0, ' ' * (self.__width - 1), curses.color_pair(3))
            self.__std_scr.addstr(self.__height - 1, 0, status_bar, curses.color_pair(3))
            input_str = self.__input_wrapper(y_offset, x_offset, self.__width - x_offset - 1)
            return input_str.decode("utf-8")
        return self.draw_app(__draw_modal_prompt)

    def draw_input(self, input_items: [dict], state_name: str):
        current_index = 0

        def __draw_input_instance(key: int):
            nonlocal current_index
            current_index = self.__calculate_current_index(key, current_index, len(input_items))
            y_pos = 4
            self.__draw_subtitle(state_name)
            for (i, item) in enumerate(input_items):
                item_value = item["value"] if item["value"] is not None else '<empty>'
                if i == current_index:
                    self.__std_scr.addstr(y_pos + i, 0, f'{item["name"]}: {item_value}', curses.color_pair(2))
                else:
                    self.__std_scr.addstr(y_pos + i, 0, f'{item["name"]}: {item_value}')
            self.__std_scr.addstr(y_pos + len(input_items), 0, '-' * self.__width)
            color_palette = 0
            save_button_sign = ' * '
            status_bar = "Press 'q' to exit | Press any key to go back | "
            hint_input = 'Press Enter to change data'
            hint_save = 'Press Enter to proceed'
            if current_index == len(input_items):
                color_palette = curses.color_pair(2)
                save_button_sign = '-> '
                status_bar += hint_save
            else:
                status_bar += hint_input
            self.__std_scr.addstr(y_pos + len(input_items) + 1, 0,
                                  f'{save_button_sign} Confirm entered data', color_palette)
            self.__std_scr.addstr(self.__height - 1, 0, ' ' * (self.__width - 1), curses.color_pair(3))
            self.__std_scr.addstr(self.__height - 1, 0, status_bar, curses.color_pair(3))
            if (key == curses.KEY_ENTER or key == ord('\n')) and current_index < len(input_items):
                x_offset = len(input_items[current_index]["name"]) + 2
                self.__std_scr.addstr(y_pos + current_index, x_offset, ' ' * (self.__width - x_offset))
                input_str = self.__input_wrapper(y_pos + current_index, x_offset, self.__width - x_offset - 1)
                value = input_str.decode("utf-8")
                if value == "":
                    value = None
                input_items[current_index]["value"] = value
                return ConsoleCommands.STANDBY
            elif (key == curses.KEY_ENTER or key == ord('\n')) and current_index == len(input_items):
                # self.__prev_index = self.__state.pop()
                return ConsoleCommands.CONFIRM
            elif key == curses.KEY_BACKSPACE:
                self.__prev_index = self.__state.pop()
                return ConsoleCommands.GO_BACK
            else:
                return ConsoleCommands.STANDBY
        return self.draw_app(__draw_input_instance)

    def draw_filtering(self, cost_from: Decimal, cost_to: Decimal, names: [str],
                       sender_i: int = None, recipient_i: int = None):
        result = {'min': cost_from, 'max': cost_to, 'sender_i': sender_i, 'recipient_i': recipient_i}
        current_row = 0
        editing_sender = False
        editing_recipient = False

        def __draw_filtering_instance(key: int):
            nonlocal current_row, editing_sender, editing_recipient, result
            if not editing_sender and not editing_recipient:
                current_row = self.__calculate_current_index(key, current_row, 4)
            if editing_sender:
                result['sender_i'] = self.__calculate_current_index(key, result['sender_i'], len(names) - 1)
            if editing_recipient:
                result['recipient_i'] = self.__calculate_current_index(key, result['recipient_i'], len(names) - 1)
            self.__draw_subtitle('Search by multiple attributes of two entities')
            y_pos = y_start = 4
            min_cost_prompt = "From shipping cost, ₴:"
            max_cost_prompt = "To shipping cost, ₴:"
            prompts = [min_cost_prompt, max_cost_prompt]
            values = [result['min'], result['max']]
            for i, prompt in enumerate(prompts):
                if i == current_row:
                    self.__std_scr.addstr(y_pos + i, 0, f'{prompt} {values[i]}', curses.color_pair(2))
                else:
                    self.__std_scr.addstr(y_pos + i, 0, f'{prompt} {values[i]}')
            y_pos += len(prompts)
            self.__std_scr.addstr(y_pos, 0, '*' * self.__width)
            y_pos += 1
            x_pos_half = self.__width // 2
            send_color = curses.color_pair(2) if current_row == 2 else 0
            resp_color = curses.color_pair(2) if current_row == 3 else 0
            self.__std_scr.addstr(y_pos, 0, 'Choose sender name:', send_color)
            self.__std_scr.addstr(y_pos, x_pos_half, 'Choose recipient name:', resp_color)
            self.__std_scr.addstr(y_pos + 1, 0, '-' * self.__width)
            y_pos += 2
            list_max_len = 12
            start_i_sender = result['sender_i'] - list_max_len + 1 if result['sender_i'] >= list_max_len else 0
            start_i_recipient = result['recipient_i'] - list_max_len + 1 if result['recipient_i'] >= list_max_len else 0
            current_sender_list = names[start_i_sender:start_i_sender + list_max_len]
            current_recipient_list = names[start_i_recipient:start_i_recipient + list_max_len]
            for i, name in enumerate(current_sender_list):
                if start_i_sender + i == result['sender_i']:
                    self.__std_scr.addstr(y_pos + i, 0, name, curses.color_pair(1))
                else:
                    self.__std_scr.addstr(y_pos + i, 0, name)
            for i, name in enumerate(current_recipient_list):
                if start_i_recipient + i == result['recipient_i']:
                    self.__std_scr.addstr(y_pos + i, x_pos_half, name, curses.color_pair(1))
                else:
                    self.__std_scr.addstr(y_pos + i, x_pos_half, name)
            self.__std_scr.addstr(y_pos + list_max_len, 0, '-' * self.__width)
            color_palette = 0
            save_button_sign = ' * '
            status_bar = "Press 'q' to exit | Press any key to go back | "
            hint_input = 'Press Enter to change data'
            hint_save = 'Press Enter to proceed'
            if current_row == len(prompts) + 2:
                color_palette = curses.color_pair(2)
                save_button_sign = '-> '
                status_bar += hint_save
            else:
                status_bar += hint_input
            self.__std_scr.addstr(self.__height - 1, 0, ' ' * (self.__width - 1), curses.color_pair(3))
            self.__std_scr.addstr(self.__height - 1, 0, status_bar, curses.color_pair(3))
            self.__std_scr.addstr(self.__height - 2, 0,
                                  f'{save_button_sign} Confirm entered data', color_palette)
            if (key == curses.KEY_ENTER or key == ord('\n')) and current_row < len(prompts):
                x_offset = len(prompts[current_row]) + 1
                self.__std_scr.addstr(y_start + current_row, x_offset, ' ' * (self.__width - x_offset))
                input_str = self.__input_wrapper(y_start + current_row, x_offset, self.__width - x_offset - 1)
                value = input_str.decode("utf-8")
                if current_row == 0:
                    result['min'] = value
                else:
                    result['max'] = value
                return ConsoleCommands.STANDBY
            elif (key == curses.KEY_ENTER or key == ord('\n')) and current_row < len(prompts) + 2:
                if current_row == 2:
                    editing_sender = not editing_sender
                elif current_row == 3:
                    editing_recipient = not editing_recipient
                return ConsoleCommands.STANDBY
            elif (key == curses.KEY_ENTER or key == ord('\n')) and current_row == len(prompts) + 2:
                # self.__prev_index = self.__state.pop()
                return result
            elif key == curses.KEY_BACKSPACE:
                self.__prev_index = self.__state.pop()
                return ConsoleCommands.GO_BACK
            else:
                return ConsoleCommands.STANDBY

        return self.draw_app(__draw_filtering_instance)

    def draw_app(self, draw_main: Callable[[int], int or str]):
        self.__std_scr.clear()
        self.__std_scr.refresh()
        key = 0
        title = self.__name
        status_bar = f"Press 'q' to exit | Press Enter to choose option | " \
                     f"Press Backspace to go back "
        while key != ord('q') and not self.__should_exit:
            self.__std_scr.clear()
            self.__height, self.__width = self.__std_scr.getmaxyx()
            start_x_title = (self.__width - len(title)) // 2
            self.__std_scr.addstr(0, start_x_title, title, curses.color_pair(1) | curses.A_BOLD)
            self.__std_scr.addstr(1, 0, '═' * self.__width, curses.color_pair(1) | curses.A_BOLD)
            self.__std_scr.addstr(self.__height - 1, 0, ' ' * (self.__width - 1), curses.color_pair(3))
            self.__std_scr.addstr(self.__height - 1, 0, status_bar, curses.color_pair(3))
            res = draw_main(key)
            if isinstance(res, dict) or isinstance(res, str) \
                    or (isinstance(res, int) and res != ConsoleCommands.STANDBY):
                return res
            self.__std_scr.refresh()
            key = self.__std_scr.getch()
        self.__should_exit = True
        sys.exit(0)

    def __draw_subtitle(self, subtitle: str):
        start_x = (self.__width - len(subtitle)) // 2
        self.__std_scr.addstr(2, start_x, subtitle.upper(), curses.color_pair(4))
        self.__std_scr.addstr(3, 0, '─' * self.__width, curses.color_pair(4))

    def __input_wrapper(self, y_offset, x_offset, width):
        curses.curs_set(1)
        curses.echo()
        input_str = self.__std_scr.getstr(y_offset, x_offset, width)
        curses.noecho()
        curses.curs_set(0)
        return input_str

    @staticmethod
    def __calculate_current_index(key: int, current_index: int, maximum_index: int):
        if key == curses.KEY_DOWN:
            current_index += 1
        elif key == curses.KEY_UP:
            current_index -= 1
        current_index = max(0, current_index)
        current_index = min(maximum_index, current_index)
        return current_index
