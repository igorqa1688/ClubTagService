import pytest
import tag_service_pb2_grpc
from tag_service_pb2 import CreateClubTagRequest, UpdateClubTagRequest, GUID, GetTagRequest, GetClubTagsRequest
from tag_service_pb2 import RemoveTagRequest
from functions import generate_guid, generate_random_string, generate_hex_color
from requests import create_club_tag, get_tag, get_club_tags, update_club_tag, remove_tag
from conftest import grpc_channel


# Только обязательные поля
def test_create_club_tag(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_hex_color()
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = CreateClubTagRequest(
        club_guid=GUID(value=f"{club_guid}"),
        name=name,
        color=color)

    response = stub.CreateClubTag(request)

    assert len(response.tag.guid.value) == 36
    assert response.tag.name == name
    assert response.tag.color == color


# name 100 символов
def test_create_club_tag_name_100_symbols(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(100)
    color = generate_hex_color()
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = CreateClubTagRequest(
        club_guid=GUID(value=f"{club_guid}"),
        name=name,
        color=color)

    response = stub.CreateClubTag(request)

    assert len(response.tag.guid.value) == 36
    assert response.tag.name == name
    assert response.tag.color == color


# name 1 символ
def test_create_club_tag_name_1_symbol(grpc_channel):
    club_guid = generate_guid()
    name = "s"
    color = generate_hex_color()
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = CreateClubTagRequest(
        club_guid=GUID(value=f"{club_guid}"),
        name=name,
        color=color)

    response = stub.CreateClubTag(request)
    assert len(response.tag.guid.value) == 36
    assert response.tag.name == name
    assert response.tag.color == color


# color не hex, длина 16 символов
def test_create_club_tag_color_not_hex(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(16)
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = CreateClubTagRequest(
        club_guid=GUID(value=f"{club_guid}"),
        name=name,
        color=color)

    response = stub.CreateClubTag(request)

    assert len(response.tag.guid.value) == 36
    assert response.tag.name == name
    assert response.tag.color == color


# color не hex, длина 1 символ
def test_create_club_tag_color_1_symbol(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = "a"
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = CreateClubTagRequest(
        club_guid=GUID(value=f"{club_guid}"),
        name=name,
        color=color)

    response = stub.CreateClubTag(request)

    assert len(response.tag.guid.value) == 36
    assert response.tag.name == name
    assert response.tag.color == color


# color не hex, с пробелом
def test_create_club_tag_color_with_spaces(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    words_count = 2
    color = ""
    for i in range(words_count):
        color += generate_random_string(3) + " "
    color = color.strip()
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = CreateClubTagRequest(
        club_guid=GUID(value=f"{club_guid}"),
        name=name,
        color=color)

    response = stub.CreateClubTag(request)
    try:
        remove_tag(response.tag.guid.value)
    except Exception as error_delete_tag:
        print(e)
    assert len(response.tag.guid.value) == 36
    assert response.tag.name == name
    assert response.tag.color == color


# club_guid не передан
def test_create_club_tag_without_club_guid(grpc_channel):
    club_guid = ""
    name = generate_random_string(12)
    color = generate_random_string(12)
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    try:
        request = CreateClubTagRequest(
            club_guid=GUID(value=f"{club_guid}"),
            name=name,
            color=color)

        response = stub.CreateClubTag(request)
        assert len(response.tag.guid.value) != 36
    except Exception as error_create_tag:
        # Распаковка ответа
        status_code = error_create_tag.code()
        grpc_details = error_create_tag.details()
        # Тэг не найден
        assert status_code.value[0] == 13
        assert grpc_details == "Internal Error. Check service logs"


# Создание тэга без названия
def test_create_club_tag_without_name(grpc_channel):
    club_guid = generate_guid()
    name = ""
    color = generate_hex_color()
    # Создание тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = CreateClubTagRequest(
            club_guid=GUID(value=f"{club_guid}"),
            name=name,
            color=color)

        response = stub.CreateClubTag(request)
        assert len(response.tag.guid.value) != 36
    except Exception as error_create_tag:
        # Распаковка ответа
        status_code = error_create_tag.code()
        grpc_details = error_create_tag.details()
        # Тэг не найден
        assert status_code.value[0] == 3
        assert grpc_details == "Tag name cannot be empty"


# Создание тэга без цвета
def test_create_club_tag_without_color(grpc_channel):
    error_text = "Internal Error. Check service logs"
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = ""
    # Создание тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = CreateClubTagRequest(
            club_guid=GUID(value=f"{club_guid}"),
            name=name,
            color=color)

        response = stub.CreateClubTag(request)
        assert len(response.tag.guid.value) != 36
    except Exception as error_create_tag:
        # Распаковка ответа
        status_code = error_create_tag.code()
        grpc_details = error_create_tag.details()
        # Тэг не найден
        assert status_code.value[0] == 13
        assert grpc_details == error_text


# Создание дубля тэга в одном клубе
def test_create_club_tag_exist_name_and_color(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Создание дубля тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = CreateClubTagRequest(
            club_guid=GUID(value=f"{club_guid}"),
            name=name,
            color=color)

        response = stub.CreateClubTag(request)
        assert len(response.tag.guid.value) != 36
    except Exception as error_create_tag:
        # Распаковка ответа
        status_code = error_create_tag.code()
        grpc_details = error_create_tag.details()
        # Тэг не найден
        assert status_code.value[0] == 3
        assert grpc_details == "Tag with the same color already exists"


# Создание дубля тэга в другом клубе
def test_create_club_tags_in_different_clubs(grpc_channel):
    clubs = []
    # Генерация guid клубов в которых будут созданы тэги
    for i in range(2):
        clubs.append(generate_guid())
    # name и color создаваемых тэгов
    name = generate_random_string(12)
    color = generate_hex_color()
    created_tags = []
    # Создание тэгов в разных клубах
    for i in range(len(clubs)):
        created_tags.append(create_club_tag(clubs[i], name, color))
        assert len(created_tags[i].tag.guid.value) == 36
        assert created_tags[i].tag.name == name
        assert created_tags[i].tag.color == color
        assert created_tags[i].tag.club_guid.value == clubs[i]


# Обновление  тэга в другом клубе
def test_create_club_tags_in_different_clubs(grpc_channel):
    clubs = []
    # Генерация guid клубов в которых будут созданы тэги
    for i in range(2):
        clubs.append(generate_guid())

    created_tags = []
    # Создание тэгов в разных клубах
    for i in range(len(clubs)):
        created_tags.append(create_club_tag(clubs[i], generate_random_string(15), generate_hex_color()))
    # Получение guid тэга из клуба "B"
    updated_tag = created_tags[1].tag.guid.value
    # Обновление тэга из клуба "B" данными тэга из клуба "A"
    update_club_tag(updated_tag, created_tags[0].tag.name, created_tags[0].tag.color)
    # Получение обновленного тэга в клубе "B"
    tag_in_club_b = get_tag(updated_tag)

    # Обновлен соответствующий тэг
    assert tag_in_club_b.guid.value == updated_tag
    # Обновленное название тэга соответствует названию тэга из клуба "A"
    assert tag_in_club_b.name == created_tags[0].tag.name
    # Обновленный цвет тэга соответствует цвету тэга из клуба "A"
    assert tag_in_club_b.color == created_tags[0].tag.color


# Создание тэга в том же клубе с таким же названием
def test_create_club_tag_exist_name(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Создание дубля тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = CreateClubTagRequest(
            club_guid=GUID(value=f"{club_guid}"),
            name=name,
            color=generate_hex_color())

        response = stub.CreateClubTag(request)
        assert len(response.tag.guid.value) != 36
    except Exception as error_create_tag:
        # Распаковка ответа
        status_code = error_create_tag.code()
        grpc_details = error_create_tag.details()
        # Тэг не найден
        assert status_code.value[0] == 3
        assert grpc_details == "Tag with the same name already exists"


# Создание тэга в том же клубе с таким же цветом
def test_create_club_tag_exist_color(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Создание дубля тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = CreateClubTagRequest(
            club_guid=GUID(value=f"{club_guid}"),
            name=generate_random_string(12),
            color=color)

        response = stub.CreateClubTag(request)
        assert len(response.tag.guid.value) != 36
    except Exception as error_create_tag:
        # Распаковка ответа
        status_code = error_create_tag.code()
        grpc_details = error_create_tag.details()
        # Тэг не найден
        assert status_code.value[0] == 3
        assert grpc_details == "Tag with the same color already exists"


# Создание дубля тэга в клубе
def test_create_club_tag_exist_name_and_color(grpc_channel):
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Создание дубля тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = CreateClubTagRequest(
            club_guid=GUID(value=f"{club_guid}"),
            name=name,
            color=color)

        response = stub.CreateClubTag(request)
        assert len(response.tag.guid.value) != 36
    except Exception as error_create_tag:
        # Распаковка ответа
        status_code = error_create_tag.code()
        grpc_details = error_create_tag.details()
        # Тэг не найден
        assert status_code.value[0] == 3
        assert grpc_details == "Tag with the same color already exists"


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


# Передан несуществующий tag_guid
def test_update_club_tag_no_exist(grpc_channel):
    error_text = "Tag not found"
    # Получение guid тэга
    tag_guid = generate_guid()
    # Новые данные для обновления тэга
    new_name = generate_random_string(12)
    new_color = generate_random_string(12)
    # Обновление тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = UpdateClubTagRequest(
            guid=GUID(value=f"{tag_guid}"),
            name=new_name,
            color=new_color)

        response = stub.UpdateClubTag(request)
        assert len(response.guid.value) != 36
    except Exception as error_update_tag:
        # Распаковка ответа
        status_code = error_update_tag.code()
        grpc_details = error_update_tag.details()

        assert status_code.value[0] == 5
        assert grpc_details == error_text


# tag_guid не передан
def test_update_club_tag_without_tag_guid(grpc_channel):
    error_text = "Internal Error. Check service logs"
    # Получение guid тэга
    tag_guid = ""
    # Новые данные для обновления тэга
    new_name = generate_random_string(12)
    new_color = generate_random_string(12)
    # Обновление тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = UpdateClubTagRequest(
            guid=GUID(value=f"{tag_guid}"),
            name=new_name,
            color=new_color)

        response = stub.UpdateClubTag(request)
        assert len(response.guid.value) != 36
    except Exception as error_update_tag:
        # Распаковка ответа
        status_code = error_update_tag.code()
        grpc_details = error_update_tag.details()

        assert status_code.value[0] == 13
        assert grpc_details == error_text


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


# Обновление тэга: name 100 символов
def test_update_club_tag_name_100_symbols(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(99)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_name = generate_random_string(100)
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


# Обновление тэга: name 1 символ
def test_update_club_tag_name_1_symbol(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_name = "j"
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


# Обновление тэга: color 16 символов
def test_update_club_tag_color_16_symbols(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(99)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_color = generate_random_string(16)
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


# Обновление тэга: color 16 символов
def test_update_club_tag_color_1_symbol(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(99)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_color = ";"
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


# Изменение name тэга на name существующего тэга в этом же клубе
def test_update_club_tag_exist_name(grpc_channel):
    error_text = "Tag with the same name already exists"
    # Данные для создания тэга
    club_guid = generate_guid()
    created_tags = []
    # Создание тэгов
    for i in range(2):
        created_tags.append(create_club_tag(club_guid, generate_random_string(20), generate_hex_color()))
    # Получение guid обновляемого тэга
    updated_tag_guid = created_tags[1].tag.guid.value

    # Получение name для обновления
    name = created_tags[0].tag.name
    # Новые данные для обновления тэга
    new_color = generate_hex_color()

    # Обновление тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = UpdateClubTagRequest(
            guid=GUID(value=f"{updated_tag_guid}"),
            name=name,
            color=new_color)

        response = stub.UpdateClubTag(request)
        assert response.tag.color != name
    except Exception as error_update_tag:
        # Распаковка ответа
        status_code = error_update_tag.code()
        grpc_details = error_update_tag.details()

        assert status_code.value[0] == 3
        assert grpc_details == error_text


# Изменение color тэга на color существующего тэга в этом же клубе
def test_update_club_tag_exist_color(grpc_channel):
    error_text = "Tag with the same color already exists"
    # Данные для создания тэга
    club_guid = generate_guid()
    created_tags = []
    # Создание тэгов
    for i in range(2):
        created_tags.append(create_club_tag(club_guid, generate_random_string(20), generate_hex_color()))
    # Получение guid обновляемого тэга
    updated_tag_guid = created_tags[1].tag.guid.value

    # Получение name для обновления
    color = created_tags[0].tag.color
    # Новые данные для обновления тэга
    new_name = generate_random_string(15)

    # Обновление тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = UpdateClubTagRequest(
            guid=GUID(value=f"{updated_tag_guid}"),
            name=new_name,
            color=color)

        response = stub.UpdateClubTag(request)
        assert response.tag.color == color
    except Exception as error_update_tag:
        # Распаковка ответа
        status_code = error_update_tag.code()
        grpc_details = error_update_tag.details()

        assert status_code.value[0] == 3
        assert grpc_details == error_text


# Изменение name, color тэга на name, color существующего тэга в этом же клубе
def test_update_club_tag_exist_name_and_color(grpc_channel):
    error_text = "Tag with the same name already exists"
    # Данные для создания тэга
    club_guid = generate_guid()
    created_tags = []
    # Создание тэгов
    for i in range(2):
        created_tags.append(create_club_tag(club_guid, generate_random_string(20), generate_hex_color()))
    # Получение guid обновляемого тэга
    updated_tag_guid = created_tags[1].tag.guid.value

    # Получение color для обновления
    color = created_tags[0].tag.color
    # Получение name для обновления
    name = created_tags[0].tag.name

    # Обновление тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = UpdateClubTagRequest(
            guid=GUID(value=f"{updated_tag_guid}"),
            name=name,
            color=color)

        response = stub.UpdateClubTag(request)
        assert response.tag.name != name
    except Exception as error_update_tag:
        # Распаковка ответа
        status_code = error_update_tag.code()
        grpc_details = error_update_tag.details()

        assert status_code.value[0] == 3
        assert grpc_details == error_text


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


# Обновление тэга: без названия
def test_update_club_tag_without_name(grpc_channel):
    error_text = "Tag name cannot be empty"
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_hex_color()
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_name = ""
    # Обновление тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = UpdateClubTagRequest(
            guid=GUID(value=f"{tag_guid}"),
            name=new_name,
            color=color)

        response = stub.UpdateClubTag(request)
        assert response.tag.name != name
    except Exception as error_update_tag:
        # Распаковка ответа
        status_code = error_update_tag.code()
        grpc_details = error_update_tag.details()

        assert status_code.value[0] == 3
        assert grpc_details == error_text


# Обновление тэга: без цвета
def test_update_club_tag_without_color(grpc_channel):
    error_text = "Internal Error. Check service logs"
    # Данные для создания тэга
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(15)
    # Создание тэга
    created_tag = create_club_tag(club_guid, name, color)
    # Получение guid созданного тэга
    tag_guid = created_tag.tag.guid.value
    # Новые данные для обновления тэга
    new_color = ""
    # Обновление тэга
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    try:
        request = UpdateClubTagRequest(
            guid=GUID(value=f"{tag_guid}"),
            name=name,
            color=new_color)

        response = stub.UpdateClubTag(request)
        assert response.tag.guid.value != 36
    except Exception as error_update_tag:
        # Распаковка ответа
        status_code = error_update_tag.code()
        grpc_details = error_update_tag.details()

        assert status_code.value[0] == 13
        assert grpc_details == error_text


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

    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)

    request = GetTagRequest(
        tag_id=GUID(value=f"{tag_guid}"))

    response = stub.GetTag(request)

    assert len(tag_guid) == 36
    assert tag_guid == response.guid.value

    assert tag_club_guid == response.club_guid.value
    assert tag_name == response.name
    assert tag_color == response.color


# В клубе 1 тэг
def test_get_club_tags_1_tag(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    tags_count = 1
    tags_in_club = []

    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    for i in range(tags_count):
        name = generate_random_string(12)
        color = generate_hex_color()
        # Создание тэга
        created_tag = create_club_tag(club_guid, name, color)
        tags_in_club.append(created_tag)
        # Распаковка созданного тэга
        tag_guid = created_tag.tag.guid.value
        tag_club_guid = created_tag.tag.club_guid.value
        tag_name = created_tag.tag.name
        tag_color = created_tag.tag.color

        request = GetClubTagsRequest(
            club_guid=GUID(value=f"{club_guid}"))

        response = stub.GetClubTags(request)

        created_tags = response.tags

        assert len(tag_guid) == 36
        assert created_tags[i].guid.value == tag_guid
        assert tag_club_guid == created_tags[i].club_guid.value
        assert tag_name == created_tags[i].name
        assert tag_color == created_tags[i].color

    assert len(created_tags) == tags_count


# В клубе 2 тэга
def test_get_club_tags_2_tags(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    tags_count = 2
    tags_in_club = []

    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    for i in range(tags_count):
        name = generate_random_string(12)
        color = generate_hex_color()
        # Создание тэга
        created_tag = create_club_tag(club_guid, name, color)
        tags_in_club.append(created_tag)
        # Распаковка созданного тэга
        tag_guid = created_tag.tag.guid.value
        tag_club_guid = created_tag.tag.club_guid.value
        tag_name = created_tag.tag.name
        tag_color = created_tag.tag.color

        request = GetClubTagsRequest(
            club_guid=GUID(value=f"{club_guid}"))

        response = stub.GetClubTags(request)

        created_tags = response.tags

        assert len(tag_guid) == 36
        assert created_tags[i].guid.value == tag_guid
        assert tag_club_guid == created_tags[i].club_guid.value
        assert tag_name == created_tags[i].name
        assert tag_color == created_tags[i].color

    assert len(created_tags) == tags_count


# В клубе 2 тэга с одним названием но разным регистром
def test_create_club_tags_2_name_different_register():
    # Данные для создания тэга
    club_guid = generate_guid()

    name = generate_random_string(12)
    name = name.upper()
    color = generate_hex_color()
    # Создание первого тэга
    create_club_tag(club_guid, name, color)

    second_tag = create_club_tag(club_guid, name.lower(), generate_hex_color())

    assert len(second_tag.tag.guid.value) == 36
    assert second_tag.tag.name == name.lower()


# Обновление тэга. В клубе 2 тэга с одним названием но разным регистром
def test_update_club_tags_2_name_different_register():
    # Данные для создания тэга
    club_guid = generate_guid()

    tags_in_club = []
    # Создание первого тэга
    for i in range(2):
        # name всех создаваемых тэгов приводятся к нижнему регистру
        name = generate_random_string(12).lower()
        tags_in_club.append(create_club_tag(club_guid, name, generate_hex_color()))

    # Получение name первого тэга в клубе
    tag_name_first = tags_in_club[0].tag.name
    # Приведение полученного имени к верхнему регистру
    tag_name_upper = tag_name_first.upper()
    # Получение guid второго тэга в клубе, guid тэга для обновления
    tag_guid_second = tags_in_club[1].tag.guid.value
    # Обновление второго тэга с присвоением тэгу name первого тэга в uppercase
    updated_tag = update_club_tag(tag_guid_second, tag_name_upper, generate_hex_color())

    assert updated_tag.name == tag_name_upper


# Обновление тэга. В клубе 2 тэга с одним color но разным регистром
def test_update_club_tags_2_color_different_register():
    # Данные для создания тэга
    club_guid = generate_guid()

    tags_in_club = []
    # Создание первого тэга
    for i in range(2):
        # color всех создаваемых тэгов приводятся к нижнему регистру
        color = generate_hex_color().lower()
        tags_in_club.append(create_club_tag(club_guid, generate_random_string(10), color))

    # Получение color первого тэга в клубе
    tag_color_first = tags_in_club[0].tag.color
    # Приведение полученного color к верхнему регистру
    tag_color_upper = tag_color_first.upper()
    # Получение guid второго тэга в клубе, guid тэга для обновления
    tag_guid_second = tags_in_club[1].tag.guid.value
    # Обновление второго тэга с присвоением тэгу color первого тэга в uppercase
    updated_tag = update_club_tag(tag_guid_second, tags_in_club[1].tag.name, tag_color_upper)

    assert updated_tag.color == tag_color_upper


# В клубе 2 тэга с одним цветом но цвет в разном регистре
def test_create_club_tags_2_color_different_register():
    # Данные для создания тэга
    club_guid = generate_guid()

    name = generate_random_string(12)
    name = name.upper()
    color = generate_hex_color()
    color = color.lower()
    # Создание первого тэга
    create_club_tag(club_guid, name, color)

    second_tag = create_club_tag(club_guid, generate_random_string(12), color.upper())

    assert len(second_tag.tag.guid.value) == 36
    assert second_tag.tag.color == color.upper()


# В клубе 10 тэгов
def test_get_club_tags_10_tags(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()
    tags_count = 10
    tags_in_club = []
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    for i in range(tags_count):
        name = generate_random_string(12)
        color = generate_hex_color()
        # Создание тэга
        created_tag = create_club_tag(club_guid, name, color)
        tags_in_club.append(created_tag)
        # Распаковка созданного тэга
        tag_guid = created_tag.tag.guid.value
        tag_club_guid = created_tag.tag.club_guid.value
        tag_name = created_tag.tag.name
        tag_color = created_tag.tag.color

        request = GetClubTagsRequest(
            club_guid=GUID(value=f"{club_guid}"))

        response = stub.GetClubTags(request)

        created_tags = response.tags

        assert len(tag_guid) == 36
        assert created_tags[i].guid.value == tag_guid
        assert tag_club_guid == created_tags[i].club_guid.value
        assert tag_name == created_tags[i].name
        assert tag_color == created_tags[i].color

    assert len(created_tags) == tags_count


# В клубе нет тэгов
def test_get_club_tags_without_tags(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()

    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)

    request = GetClubTagsRequest(
        club_guid=GUID(value=f"{club_guid}"))

    response = stub.GetClubTags(request)

    assert len(response.tags) == 0


# Удаление тэга
def test_remove_tag(grpc_channel):
    # Данные для создания тэга
    club_guid = generate_guid()

    for i in range(2):
        # Создание тэга
        name = generate_random_string(12)
        color = generate_hex_color()
        created_tag = create_club_tag(club_guid, name, color)

    # Распаковка созданного тэга
    tag_guid = created_tag.tag.guid.value

    # Удаление тэга
    stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
    request = RemoveTagRequest(
        tag_id=GUID(value=f"{tag_guid}"))
    stub.RemoveTag(request)

    # Получение удаленного тэга
    get_removed_tag = get_tag(club_guid)
    # Распаковка ответа
    status_code = get_removed_tag.code()
    grpc_details = get_removed_tag.details()
    # Тэг не найден
    assert status_code.value[0] == 5
    assert grpc_details == "Tag not found"

    # Тэг не найден в клубе
    get_removed_tag_in_club = get_club_tags(club_guid)
    for i in range(len(get_removed_tag_in_club.tags)):
        assert tag_guid not in get_removed_tag_in_club.tags[i].guid.value


# guid тэга не передан в запрос
def test_remove_tag_guid_equal_null(grpc_channel):
    # Генерация несуществующего тэга
    tag_guid = ""
    error_text = "Internal Error. Check service logs"
    # Удаление тэга
    try:
        stub = tag_service_pb2_grpc.TagServiceStub(grpc_channel)
        request = RemoveTagRequest(
        tag_id=GUID(value=f"{tag_guid}"))
        stub.RemoveTag(request)
    except Exception as error_remove_tag:
        # Распаковка ответа
        status_code = error_remove_tag.code()
        grpc_details = error_remove_tag.details()

        assert status_code.value[0] == 13
        assert grpc_details == error_text
