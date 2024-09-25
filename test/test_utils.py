import socket
from concurrent import futures
from pathlib import Path
from typing import Union, Any

import grpc
import jsonpickle


class TestUtils:

    @staticmethod
    def decode_jsonpickle_file(file_path: Union[Path, str]) -> Any:
        with open(file_path, "r") as file:
            dumped = file.read()
        return jsonpickle.decode(dumped)

    @staticmethod
    def grpc_address() -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        return f'localhost:{sock.getsockname()[1]}'

    @classmethod
    def set_up_server(cls):
        grpc_address: str = cls.grpc_address()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1), compression=grpc.Compression.NoCompression)
        server.add_insecure_port(grpc_address)
        return server, grpc_address
