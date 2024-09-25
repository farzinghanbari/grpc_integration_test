import logging
from typing import Union

from injector import inject

from protobuf.grpc_integration_test.contact_pb2 import GetAllRequest, GetAllResponse, AddRequest, AddResponse
from protobuf.grpc_integration_test.contact_pb2_grpc import ContactServiceServicer
from src.service.core.service_app_service_contract.data_model.contact.contact_data_model import ContactDataModel
from src.service.core.service_app_service_contract.interface.contact_service.icontact_service import IContactService


class ContactService(ContactServiceServicer):
    @inject
    def __init__(self, service: IContactService) -> None:
        self.__service: IContactService = service

    def GetAll(self, request: GetAllRequest, context) -> GetAllResponse:
        try:
            name: str = request.name.value or None
            data_models = self.__service.get_all(name=name)
            return self.__make_get_all_contacts_response(data_model=data_models)
        except Exception as error:
            logging.exception(error)
            return self.__make_get_all_contacts_response(message=repr(error))

    @staticmethod
    def __make_get_all_contacts_response(data_model: Union[list[ContactDataModel], None] = None,
                                         message: str = None) -> GetAllResponse:
        response = GetAllResponse()
        if message:
            response.message.value = message
        if data_model:
            for contact in data_model:
                data = response.data.add()
                data.id = contact.id
                data.name = contact.name
        return response

    def Add(self, request: AddRequest, context) -> AddResponse:
        try:
            name = request.name
            message: Union[str, None] = self.__service.add(name)
            return self.__make_add_contact_report_response(message)
        except Exception as error:
            logging.exception(error)
            return self.__make_add_contact_report_response(repr(error), is_success=False)

    @staticmethod
    def __make_add_contact_report_response(message: Union[str, None], is_success=True) -> AddResponse:
        response = AddResponse()
        response.is_success = is_success
        if message:
            response.message.value = message
        return response
