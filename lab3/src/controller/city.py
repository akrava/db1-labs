from controller import BaseController
from model.city import CityModel, City
from view.city import CityView


class CityController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(CityModel(connection), CityView('cities', view_driver))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Name of city']
        values = [item.name] if isinstance(item, City) else None
        return prompts, values

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        return City([item['value'] for item in input_items if item['name'] == 'Name of city'][0])
