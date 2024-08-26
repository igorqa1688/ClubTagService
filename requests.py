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
            return "Error create_club_tag()"


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
            return "Error update_club_tag()"


if __name__ == "__main__":
    club_guid = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(5)
    created_tag = create_club_tag(club_guid, name, color)
    created_tag_guid = created_tag.tag.guid.value
    new_name = generate_random_string(12)
    new_color = generate_random_string(9)
    print(f"{new_name}\n{new_color}")
    print(created_tag_guid)
    print(update_club_tag(created_tag_guid, new_name, new_color))
