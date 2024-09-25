from dataclasses import dataclass
from typing import Union


@dataclass
class ContactDataModel:
    name: str
    id: Union[int, None] = None
