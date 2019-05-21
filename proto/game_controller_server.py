from concurrent import futures

import grpc
import time
import proto.generated.game_controller_pb2_grpc as game_controller_pb2_grpc
import proto.generated.game_controller_pb2 as game_controller_pb2


class GameControllerServer(game_controller_pb2_grpc.GameControllerServicer):
    def __init__(self, controller=None):
        self.controller = controller

    def MakeTurn(self, request, context):
        print('Request')
        response = game_controller_pb2.ServerResponse()
        response.new_field.width = 1
        response.new_field.height = 1
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_controller_pb2_grpc.add_GameControllerServicer_to_server(GameControllerServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
