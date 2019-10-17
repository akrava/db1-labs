from controller import BaseController
from model.city import CityModel, City
from view.city import CityView


class CityController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(CityModel(connection), CityView('cities', view_driver))

    @staticmethod
    def _prompt_for_item_attributes():
        return ['Name of city']

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        return City([item['value'] for item in input_items if item['name'] is 'Name of city'][0])
