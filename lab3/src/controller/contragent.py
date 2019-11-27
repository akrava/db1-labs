from controller import BaseController
from model.contragent import ContragentModel, Contragent
from view.contragent import ContragentView


class ContragentController(BaseController):
    def __init__(self, connection, view_driver):
        super().__init__(ContragentModel(connection), ContragentView('contragents', view_driver))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Name', 'Phone number']
        values = [item.name, item.phone_number] if isinstance(item, Contragent) else None
        if for_update is False:
            prompts.insert(0, 'IPN of contragent')
            if values is not None:
                values.insert(0, item.ipn)
        return prompts, values

    @staticmethod
    def _create_obj_from_input(input_items: [dict]):
        ipn = name = phone_number = None
        for item in input_items:
            if item['name'] == 'IPN of contragent':
                ipn = int(item['value'])
                if ipn <= 0:
                    raise Exception(f"IPN should be > 0, got {ipn}")
            elif item['name'] == 'Name':
                name = item['value']
            elif item['name'] == 'Phone number':
                phone_number = item['value']
        return Contragent(ipn, name, phone_number)
