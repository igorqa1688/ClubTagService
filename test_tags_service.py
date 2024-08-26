import tag_service_pb2_grpc
from tag_service_pb2 import CreateClubTagRequest, GUID
from functions import generate_guid, generate_random_string
from requests import create_club_tag


# Только обязательные поля
def test_create_club_tag(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(12)
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = CreateClubTagRequest(
        club_guid=GUID(value=f"{club_guid}"),
        name=name,
        color=color)

    response = stub.CreateClubTag(request)

    assert len(response.tag.guid.value) == 36
    assert response.tag.name == name
    assert response.tag.color == color