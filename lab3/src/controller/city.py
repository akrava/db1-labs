from controller import BaseController
from sqlalchemy.orm import Session
from view.city import CityView
from view.common import View
from model.city import City


class CityController(BaseController):
    def __init__(self, session: Session, view: View):
        super().__init__(session, City, CityView('cities', view))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Name of city']
        values = [item.name] if isinstance(item, City) else None
        return prompts, values

    @staticmethod
    def _create_dict_from_input(input_items: [dict]):
        return {'name': [item['value'] for item in input_items if item['name'] == 'Name of city'][0]}
