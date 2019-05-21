import grpc
import proto.generated.game_controller_pb2 as game_controller_pb2
import proto.generated.game_controller_pb2_grpc as game_controller_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = game_controller_pb2_grpc.GameControllerStub(channel)
        request = game_controller_pb2.ClientRequest()
        request.turn.move = game_controller_pb2.UP
        request.player_id = 1
        field = stub.MakeTurn(request)
        print(field.new_field.height, field.new_field.width)
        # call methods as follows feature = stub.GetFeature(point)


if __name__ == '__main__':
    run()
