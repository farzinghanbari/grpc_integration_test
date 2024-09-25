from typing import Union

from injector import inject

from src.service.core.service_app_service_contract.data_model.contact.contact_data_model import ContactDataModel
from src.service.core.service_app_service_contract.interface.contact_service.icontact_service import IContactService
from src.service.core.service_app_service_contract.interface.repository.contact.icontact_repository import \
    IContactRepository
from src.service.core.service_model.contact_model import ContactModel


class ContactService(IContactService):
    @inject
    def __init__(self, repository: IContactRepository):
        self.__repository: IContactRepository = repository

    def get_all(self, name: Union[str, None]) -> list[ContactDataModel]:
        models = self.__repository.get_models(name)
        return list(map(lambda d: ContactDataModel(id=d.id, name=d.name), models))

    def add(self, name: str) -> str:
        self.__repository.add(ContactModel(name=name))
        return 'contact added successfully!'
