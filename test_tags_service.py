import tag_service_pb2_grpc
from tag_service_pb2 import CreateClubTagRequest, UpdateClubTagRequest, GUID
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


# Полное обновление тэга: name, color
def test_update_club_tag(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(15)
    print(f"\nname: {name}\ncolor: {color}")
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_name = generate_random_string(12)
    new_color = generate_random_string(12)
    # Обновление тэга
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = UpdateClubTagRequest(
        guid=GUID(value=f"{tag_guid}"),
        name=new_name,
        color=new_color)

    response = stub.UpdateClubTag(request)

    assert len(response.guid.value) == 36
    assert response.guid.value == tag_guid
    assert response.name == new_name, "error update name"
    assert response.color == new_color, "error update color"