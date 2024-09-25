from contextlib import AbstractContextManager
from typing import Union

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker, DeclarativeMeta
from sqlalchemy.util import FacadeDict

from src.company_package import IDatabaseConnection
from src.sqlalchemy_base import Base


class SqliteConnection(IDatabaseConnection):
    def __init__(self, models: list = None):
        super().__init__()
        self.__engine: Engine = self.__create_engine()
        self.__migrate_tables()
        self.__session_factory = sessionmaker(self.__engine, autoflush=True)
        self.__models = models
        self.__auxiliary_session = self.__session_factory()
        self.__seed_models()

    def __del__(self):
        self.__auxiliary_session.close_all()
        self.__session_factory.close_all()

    def sqlalchemy_session(self, has_transaction=False) -> Union[AbstractContextManager[Session], Session]:
        if has_transaction:
            return self.__session_factory.begin()
        return self.__session_factory(expire_on_commit=False)

    def query_session(self):
        return self.__auxiliary_session

    def __seed_models(self) -> None:
        if self.__models:
            with self.__session_factory.begin() as session:
                session.add_all(self.__models)
                session.commit()

    def __contains_any_tables(self) -> bool:
        with self.__session_factory() as session:
            tables = session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).all()
        return tables != []

    def __create_engine(self) -> Engine:
        return create_engine(f'sqlite:///file:?mode=memory&cache=shared&uri=true', )

    def __migrate_tables(self) -> None:
        self.__base_model: DeclarativeMeta = Base
        self.__delete_extra_metadata_from_models(self.__base_model)
        self.__delete_schema_from_tables_metadata_of_base_tables(self.__base_model)
        self.__base_model.metadata.reflect(self.__engine, schema=None)
        self.__base_model.metadata.create_all(self.__engine)

    @staticmethod
    def __delete_extra_metadata_from_models(base_model: DeclarativeMeta) -> None:
        for model in base_model.__subclasses__():
            if _ := getattr(model, '__table_args__', None):
                delattr(model, '__table_args__')
            table = getattr(model, '__table__', None)
            if table is not None:
                if _ := getattr(table, 'schema', False):
                    setattr(table, 'schema', None)
                    setattr(model, '__table__', table)

    @staticmethod
    def __delete_schema_from_tables_metadata_of_base_tables(base_model: DeclarativeMeta) -> None:
        current_schema = ''
        if schemas := list(base_model.metadata._schemas):
            current_schema = schemas[0]
        tables = {}
        for table in base_model.metadata.tables:
            tables[table.replace(f'{current_schema}.', '')] = base_model.metadata.tables[table]
        base_model_metadata_tables = FacadeDict(tables)
        setattr(base_model.metadata, 'tables', base_model_metadata_tables)
