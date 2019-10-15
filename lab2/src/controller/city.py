from controller import BaseController
from model.city import CityModel
from view.city import CityView


class CityController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(CityModel(connection), CityView('cities', view_driver))
