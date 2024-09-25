from pathlib import Path

import grpc
from grpc._server import _Server
from injector import singleton
from pytest import fixture, mark
from sqlalchemy import select, text

from protobuf.grpc_integration_test.contact_pb2 import AddRequest, AddResponse
from protobuf.grpc_integration_test.contact_pb2_grpc import ContactServiceStub, add_ContactServiceServicer_to_server
from src.company_package import IDatabaseConnection
from src.service.service_agent.grpc_service.v1.contact.contact_service import ContactService
from src.service.core.service_model.contact_model import ContactModel
from src.service.injection import Injection
from test.sqlite_connection import SqliteConnection
from test.test_utils import TestUtils


class TestIntegrationContactService:
    @staticmethod
    @fixture
    def sqlite_db_connection(request) -> SqliteConnection:
        file_path = Path(__file__).parent.joinpath(f"data/models/{request.param}.json")
        models = TestUtils.decode_jsonpickle_file(file_path) if request.param else []
        return SqliteConnection(models=models)

    @staticmethod
    def stub(server: _Server, grpc_address: str, mocked_service: ContactService) -> ContactServiceStub:
        add_ContactServiceServicer_to_server(mocked_service, server)
        server.start()
        channel = grpc.insecure_channel(grpc_address)
        return ContactServiceStub(channel)

    @mark.parametrize('sqlite_db_connection', ['contact_models'], indirect=True)
    def test_when_adding_contacts_expect_updated_database(self, sqlite_db_connection: SqliteConnection):
        injector = Injection().injector()
        injector.binder.bind(IDatabaseConnection, sqlite_db_connection, scope=singleton)
        contact_service_v1 = injector.get(ContactService)
        server, grpc_address = TestUtils.set_up_server()
        stub = self.stub(server, grpc_address, contact_service_v1)

        with sqlite_db_connection.sqlalchemy_session() as session:
            contacts = session.execute(select(ContactModel)).scalars().all()
            assert len(contacts) == 2

        request = AddRequest(name='bob')
        response_bob: AddResponse = stub.Add(request)
        assert response_bob.is_success

        with sqlite_db_connection.sqlalchemy_session() as session:
            result = session.execute(select(ContactModel)).scalars().all()
            assert len(result) == 3

        request = AddRequest(name='jack')
        response_jack: AddResponse = stub.Add(request)
        assert response_jack.is_success

        with sqlite_db_connection.sqlalchemy_session() as session:
            result = session.execute(select(ContactModel)).scalars().all()
            assert len(result) == 4
