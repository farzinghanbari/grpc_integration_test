from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class IDatabaseConnection(ABC):
    def __init__(self) -> None:
        self.__engine: Engine

    @abstractmethod
    def sqlalchemy_session(self, has_transaction: bool = None) -> Session:
        raise NotImplementedError
