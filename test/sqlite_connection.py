from contextlib import contextmanager
from typing import Generator

from apsc.base import Base
from apsc.sql_server_database_connection.isql_server_database_connection import IMSSQLServerConnection
from sqlalchemy import Engine, create_engine, text, StaticPool
from sqlalchemy.dialects.mssql import BIGINT, DATETIME, DATETIME2, DATE, DECIMAL, TINYINT
from sqlalchemy.dialects.sqlite import INTEGER, DATETIME as SQLITE_DATETIME, DATE as SQLITE_DATE, \
    DECIMAL as SQLITE_DECIMAL, SMALLINT
from sqlalchemy.orm import sessionmaker, DeclarativeMeta, class_mapper, scoped_session


class SqliteConnection(IMSSQLServerConnection):
    def __init__(self, models: list = None):
        super().__init__()
        self.__models = models
        self.__schema_set = set()

        self.__engine: Engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False},
                                              poolclass=StaticPool)
        self.__connection = self.__engine.connect()
        self.attach_all_the_schemas()
        session_factory = sessionmaker(autoflush=True, bind=self.__engine)
        self.__Session = scoped_session(session_factory)
        self.__migrate_tables()
        self.__seed_models()

    def attach_all_the_schemas(self):
        for model in Base.__subclasses__():
            self.__set_type_of_columns_of_sqlite_to_columns(model)
            table = getattr(model, '__table__', None)
            if table is not None:
                if schema := getattr(table, 'schema', False):
                    self.__schema_set.add(schema)
        for schema in self.__schema_set:
            self.__connection.execute(text(f"attach ':memory:' as {schema}"))

    def close(self):
        self.__Session.close_all()
        self.__connection.close()
        self.__engine.dispose()

    @contextmanager
    def ms_sql_server_session(self, has_transaction=False) -> Generator:
        yield self.__Session
        if has_transaction:
            self.__Session.commit()
        self.__Session.remove()

    def get_table_names_in_schema(self, schema_name):
        with self.ms_sql_server_session() as session:
            table_names = session.execute(
                text(f"SELECT name FROM {schema_name}.sqlite_master WHERE type='table';")).scalars().all()
        return table_names

    def get_all_table_names(self):
        with self.ms_sql_server_session() as session:
            table_names = session.execute(text(f"SELECT name FROM sqlite_master WHERE type='table';")).scalars().all()

        for schema_name in self.__schema_set:
            schema_tables = self.get_table_names_in_schema(schema_name)
            for table_name in schema_tables:
                table_names.append(f'{schema_name}.{table_name}')
        return table_names

    def __seed_models(self) -> None:
        if self.__models:
            with self.ms_sql_server_session() as session:
                session.add_all(self.__models)
                session.commit()

    def __migrate_tables(self) -> None:
        self.__base_model: DeclarativeMeta = Base
        self.__base_model.metadata.create_all(self.__engine)

    def __set_type_of_columns_of_sqlite_to_columns(self, model):
        mapper = class_mapper(model)
        for column in mapper.columns:
            self.__get_sqlite_type_for_column(column)

    @staticmethod
    def __get_sqlite_type_for_column(column):
        column_type = column.type
        if isinstance(column_type, BIGINT):
            column.type = INTEGER()
        elif isinstance(column_type, DATETIME):
            column.type = SQLITE_DATETIME()
        elif isinstance(column_type, DATETIME2):
            column.type = SQLITE_DATETIME()
        elif isinstance(column_type, DATE):
            column.type = SQLITE_DATE()
        elif isinstance(column_type, DECIMAL):
            column.type = SQLITE_DECIMAL()
        elif isinstance(column_type, TINYINT):
            column.type = SMALLINT()
