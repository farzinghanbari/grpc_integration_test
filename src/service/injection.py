from injector import Injector

from src.service.core.service_app_service.contact_service.contact_service import ContactService
from src.service.core.service_app_service_contract.interface.contact_service.icontact_service import IContactService
from src.service.core.service_app_service_contract.interface.repository.contact.icontact_repository import \
    IContactRepository
from src.service.infrastructure.repository.contact.contact_repository import ContactRepository


class Injection:
    def injector(self):
        injector: Injector = Injector()
        self.__bind(injector)
        return injector

    @staticmethod
    def __bind(injector: Injector):
        injector.binder.bind(IContactService, ContactService)
        injector.binder.bind(IContactRepository, ContactRepository)
