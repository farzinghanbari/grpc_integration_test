from typing import Union

from src.company_package import IDatabaseConnection
from injector import inject
from sqlalchemy import select, literal

from src.service.core.service_app_service_contract.interface.repository.contact.icontact_repository import \
    IContactRepository
from src.service.core.service_model.contact_model import ContactModel


class ContactRepository(IContactRepository):
    @inject
    def __init__(self, database_connection: IDatabaseConnection) -> None:
        self.__database_connection: IDatabaseConnection = database_connection

    def add(self, contact_model: ContactModel) -> None:
        with self.__database_connection.sqlalchemy_session(has_transaction=True) as session:
            session.add(contact_model)
            session.flush()
            session.commit()

    def get_models(self, name: Union[str, None]) -> list[ContactModel]:
        with self.__database_connection.sqlalchemy_session() as session:
            query = select(ContactModel).order_by(ContactModel.id)
            query = query.filter_by(name=literal(name)) if name else query
            all_data = session.execute(query).scalars().all()
            return list(all_data)
