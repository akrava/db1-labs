from view.reweightings import ReweightingsView
from model.reweightings import Reweightings
from controller import BaseController
from settings import ConsoleCommands
from sqlalchemy.orm import Session
from view.common import View
from typing import Callable


class ReweightingsController(BaseController):
    def __init__(self, session: Session, view: View):
        super().__init__(session, Reweightings, ReweightingsView('reweightings', view))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Date inspected (DD.MM.YYYY)', 'Weight before (g)', 'Weight after (g)', 'Goods ID']
        values = [item.date_inspection.strftime("%d.%m.%Y"), item.weight_before, item.weight_after, item.parcel_id] \
            if isinstance(item, Reweightings) else None
        return prompts, values

    def choose_operation(self, previous_state: Callable = None):
        if previous_state is not None:
            self._cb_show_prev_state = previous_state
        list_operations = ['Read', 'List all']
        operation = self._view.show_operations(list_operations)
        if operation == 0:
            self.show()
        elif operation == 1:
            self.show_all()
        elif operation == ConsoleCommands.GO_BACK:
            self._cb_show_prev_state()

    @staticmethod
    def _create_dict_from_input(input_items: [dict]):
        pass
