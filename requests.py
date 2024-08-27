import grpc
import tag_service_pb2
import tag_service_pb2_grpc
from functions import generate_guid, generate_random_string
from global_vars import server


def create_club_tag(club_guid: str, name: str, color: str):
    with grpc.insecure_channel(server) as channel:
        stub = tag_service_pb2_grpc.TagServiceStub(channel)

        request = tag_service_pb2.CreateClubTagRequest(
            club_guid=tag_service_pb2.GUID(value=f"{club_guid}"),
            name=name,
            color=color)
        try:
            response = stub.CreateClubTag(request)
            return response
        except Exception as e:
            print(e)
            return e


def update_club_tag(guid: str, name: str, color: str):
    with grpc.insecure_channel(server) as channel:
        stub = tag_service_pb2_grpc.TagServiceStub(channel)

        request = tag_service_pb2.UpdateClubTagRequest(
            guid=tag_service_pb2.GUID(value=f"{guid}"),
            name=name,
            color=color)
        try:
            response = stub.UpdateClubTag(request)
            return response
        except Exception as e:
            print(e)
            return e


def get_tag(tag_guid: str):
    with grpc.insecure_channel(server) as channel:
        stub = tag_service_pb2_grpc.TagServiceStub(channel)

        request = tag_service_pb2.GetTagRequest(
            tag_id=tag_service_pb2.GUID(value=f"{tag_guid}"))
        try:
            response = stub.GetTag(request)
            return response
        except Exception as e:
            return e


def get_club_tags(club_guid: str):
    with grpc.insecure_channel(server) as channel:
        stub = tag_service_pb2_grpc.TagServiceStub(channel)

        request = tag_service_pb2.GetClubTagsRequest(
            club_guid=tag_service_pb2.GUID(value=f"{club_guid}"))
        try:
            response = stub.GetClubTags(request)
            return response
        except Exception as e:
            print(e)
            return e


def remove_tag(tag_guid: str):
    with grpc.insecure_channel(server) as channel:
        stub = tag_service_pb2_grpc.TagServiceStub(channel)

        request = tag_service_pb2.RemoveTagRequest(
            tag_id=tag_service_pb2.GUID(value=f"{tag_guid}"))
        try:
            response = stub.RemoveTag(request)
            return response
        except Exception as e:
            print(e)
            return e


if __name__ == "__main__":
    club_guid = generate_guid()
    tags = []
    for i in range(5):
        name = generate_random_string(12)
        color = generate_random_string(5)
        created_tag = create_club_tag(club_guid, name, color)
        tag_guid = created_tag.tag.guid.value
        tags.append((created_tag))

    created_tag_guid = created_tag.tag.guid.value
    print(created_tag)
    print(remove_tag(tag_guid))
