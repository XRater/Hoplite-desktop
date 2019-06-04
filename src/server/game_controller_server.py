import logging
import os
import pickle
import time
from concurrent import futures

import grpc

import proto.generated.game_controller_pb2 as game_controller_pb2
import proto.generated.game_controller_pb2_grpc as game_controller_pb2_grpc
from src.server.session import Session


class GameControllerServer(game_controller_pb2_grpc.GameControllerServicer):
    def __init__(self, field_file=None):
        self.LOGS_DIR = "server_logs"
        self._set_up_logs()
        self._sessions = {}
        # if field_file is not None:
        #     with open(field_file, 'rb') as file:
        #         self._dungeon = Dungeon(pickle.load(file))
        #         logging.info('Loading dungeon from file {}'.format(field_file))
        # else:
        #     self._dungeon = Dungeon(Field(30, 50))
        #     logging.info('Initializing new dungeon')
        # self._logic = Logic(self._dungeon)

    def Register(self, request, context):
        def build_response(session, player_id):
            response = game_controller_pb2.RegistrationResponse()
            response.session_id = session.id
            response.player_id = player_id
            response.dungeon = pickle.dumps(session.dungeon)
            return response

        if request.join_existing_session:
            session = self._sessions.items()[0]  # ToDo(XRATER)
        else:
            session = Session()
            self._sessions[session.id] = session

        player_id = session.add_new_player()
        return build_response(session, player_id)

    def MakeTurn(self, request, context):

        def build_response(result, dungeon):
            response = game_controller_pb2.ServerResponse()
            response.dungeon = pickle.dumps(dungeon)
            response.result = result.value
            return response

        session = self._sessions[request.session_id]
        result = session.make_turn(request.player_id, request.turn)
        #        result = self._logic.move_player(0, 1)
        return build_response(result, session.dungeon)

    def _set_up_logs(self):
        log_name = 'game_process' + time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + '.log'
        if not os.path.exists(self.LOGS_DIR):
            os.makedirs(self.LOGS_DIR)
        logging.basicConfig(filename=os.path.join(self.LOGS_DIR, log_name), format='%(levelname)s:%(message)s',
                            level=logging.INFO)


def serve(port, field_file=None):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_controller_pb2_grpc.add_GameControllerServicer_to_server(GameControllerServer(field_file), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
