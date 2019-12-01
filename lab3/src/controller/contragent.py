from view.contragent import ContragentView
from model.contragent import Contragent
from controller import BaseController
from sqlalchemy.orm import Session
from view.common import View


class ContragentController(BaseController):
    def __init__(self, session: Session, view: View):
        super().__init__(session, Contragent, ContragentView('contragents', view))

    @staticmethod
    def _prompt_values_for_input(item: object = None, for_update: bool = False):
        prompts = ['Name', 'Phone number']
        values = [item.name, item.phone_number] if isinstance(item, Contragent) else None
        if for_update is False:
            prompts.insert(0, 'IPN of contragent')
            if values is not None:
                values.insert(0, item.ipn.__str__())
        return prompts, values

    @staticmethod
    def _create_dict_from_input(input_items: [dict]):
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
        return {'ipn': ipn, 'name': name, 'phone_number': phone_number}
