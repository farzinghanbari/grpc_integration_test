from abc import ABC, abstractmethod
from typing import Union

from src.service.core.service_app_service_contract.data_model.contact.contact_data_model import ContactDataModel


class IContactService(ABC):
    @abstractmethod
    def get_all(self, name: Union[str, None]) -> list[ContactDataModel]:
        raise NotImplementedError

    @abstractmethod
    def add(self, name: str) -> str:
        raise NotImplementedError
