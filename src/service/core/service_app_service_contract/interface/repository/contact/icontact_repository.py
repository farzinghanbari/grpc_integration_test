from abc import ABC, abstractmethod
from typing import Union

from src.service.core.service_model.contact_model import ContactModel


class IContactRepository(ABC):
    @abstractmethod
    def get_models(self, name: Union[str, None]) -> list[ContactModel]:
        raise NotImplementedError

    @abstractmethod
    def add(self, contact_model: ContactModel) -> None:
        raise NotImplementedError
