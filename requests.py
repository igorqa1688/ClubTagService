import grpc
import tag_service_pb2
import tag_service_pb2_grpc
from functions import generate_guid, generate_random_string
from global_vars import server


def create_club_tag(club_id: str, name: str, color: str):
    with grpc.insecure_channel(server) as channel:
        stub = tag_service_pb2_grpc.TagServiceStub(channel)
        request = tag_service_pb2.CreateClubTagRequest(
            club_id=club_id,
            name=name,
            color=color)
        try:
            response = stub.CreateClubTag(request)
            return response
        except Exception as e:
            print(e)
            return "Error create_club_tag()"


if __name__ == "__main__":
    club_id = generate_guid()
    name = generate_random_string(12)
    color = generate_random_string(5)
    create_club_tag(club_id, name, color)