import pytest
import tag_service_pb2_grpc
from tag_service_pb2 import CreateClubTagRequest, UpdateClubTagRequest, GUID
from functions import generate_guid, generate_random_string, generate_hex_color
from requests import create_club_tag
from conftest import grpc_channel


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

    assert club_guid == response.club_guid.value
    assert len(response.guid.value) == 36
    assert response.guid.value == tag_guid
    assert response.name == new_name
    assert response.color == new_color


# Обновление тэга: name
def test_update_club_tag_name(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(15)
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_name = generate_random_string(12)
    # Обновление тэга
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = UpdateClubTagRequest(
        guid=GUID(value=f"{tag_guid}"),
        name=new_name,
        color=color)

    response = stub.UpdateClubTag(request)

    assert club_guid == response.club_guid.value
    assert len(response.guid.value) == 36
    assert response.guid.value == tag_guid
    assert response.name == new_name
    assert response.color == color


# Обновление тэга: name с пробелами
def test_update_club_tag_name(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(15)
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    words_count = 2
    new_name = ""
    for i in range(words_count):
        new_name += generate_random_string(12)+" "
    new_name = new_name.strip()

    # Обновление тэга
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = UpdateClubTagRequest(
        guid=GUID(value=f"{tag_guid}"),
        name=new_name,
        color=color)

    response = stub.UpdateClubTag(request)

    assert club_guid == response.club_guid.value
    assert len(response.guid.value) == 36
    assert response.guid.value == tag_guid
    assert response.name == new_name
    assert response.color == color


# Обновление тэга: color
def test_update_club_tag_color(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(15)
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_color = generate_hex_color()
    # Обновление тэга
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = UpdateClubTagRequest(
        guid=GUID(value=f"{tag_guid}"),
        name=name,
        color=new_color)

    response = stub.UpdateClubTag(request)

    assert club_guid == response.club_guid.value
    assert len(response.guid.value) == 36
    assert response.guid.value == tag_guid
    assert response.name == name
    assert response.color == new_color


# Получение тэга
def test_get_tag(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Распаковка созданного тэга
    tag_guid = created_tag.tag.guid.value
    tag_club_guid = created_tag.tag.club_guid.value
    tag_name = created_tag.tag.name
    tag_color = created_tag.tag.color

    assert len(tag_guid) == 36
    assert tag_club_guid == club_guid
    assert tag_name == name
    assert tag_color == color


