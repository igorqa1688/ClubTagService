import grpc
import pytest
from global_vars import server


@pytest.fixture(scope="session")
def grpc_channel():
    #Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        yield channel