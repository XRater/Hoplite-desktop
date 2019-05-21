import logging
import pickle
import time
from concurrent import futures

import grpc
import pickle

import proto.generated.game_controller_pb2 as game_controller_pb2
import proto.generated.game_controller_pb2_grpc as game_controller_pb2_grpc
from src.model.dungeon import Dungeon
from src.model.field import Field
from src.model.logic.logic import Logic


class GameControllerServer(game_controller_pb2_grpc.GameControllerServicer):
    def __init__(self, field_file=None):
        if field_file is not None:
            with open(field_file, 'rb') as file:
                self._dungeon = Dungeon(pickle.load(file))
                logging.info('Loading dungeon from file {}'.format(field_file))
        else:
            self._dungeon = Dungeon(Field(30, 50))
            logging.info('Initializing new dungeon')
        self._logic = Logic(self._dungeon)

    def MakeTurn(self, request, context):

        def build_response(result, dungeon):
            response = game_controller_pb2.ServerResponse()
            response.dungeon = pickle.dumps(dungeon)
            response.result = result
            return response

        result, dungeon = self._logic.move_player(1, 0)
        return build_response(result, dungeon)


def serve(host, port, field_file=None):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_controller_pb2_grpc.add_GameControllerServicer_to_server(GameControllerServer(field_file), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
