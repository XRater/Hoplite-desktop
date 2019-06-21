import logging
import os
import pickle
import random
import time
from concurrent import futures

import grpc

import proto.generated.game_controller_pb2 as game_controller_pb2
import proto.generated.game_controller_pb2_grpc as game_controller_pb2_grpc
from src.server.session import Session


class GameControllerServer(game_controller_pb2_grpc.GameControllerServicer):
    """
    Executing grpc requests on a server.
    """
    def __init__(self):
        self.LOGS_DIR = "server_logs"
        self._set_up_logs()
        self._sessions = {}

    def Register(self, request, context):
        """
        A grpc endpoint for adding new players to the game.
        :param request: a request of type RegistrationRequest.
        :param context: grpc context
        :return: a of type RegistrationResponse.
        """
        def build_response(session, player_id):
            response = game_controller_pb2.RegistrationResponse()
            response.session_id = session.id
            response.player_id = player_id
            response.dungeon = pickle.dumps(session.dungeon)
            return response

        if request.join_existing_session and self._sessions:
            session = self._sessions[random.choice(list(self._sessions.keys()))]
        else:
            session = Session()
            self._sessions[session.id] = session

        player_id = session.add_new_player()
        logging.info(f"Added player with id {player_id} into session {session.id}")
        return build_response(session, player_id)

    def Dungeon(self, request, context):
        """
        A grpc endpoint for getting dungeon.
        :param request: a request of type DungeonRequest.
        :param context: a grpc context.
        :return: a response of type DungeonResponse.
        """
        def build_response(dungeon):
            response = game_controller_pb2.DungeonResponse()
            response.dungeon = pickle.dumps(dungeon)
            return response

        session = self._sessions[request.session_id]
        dungeon = session.dump_dungeon()
        return build_response(dungeon)

    def MakeTurn(self, request, context):
        """
        A grpc endpoint for making turns.
        :param request: a request of type ClientRequest.
        :param context: a grpc context.
        :return: a response of type ServerResponse.
        """
        def build_response(result, dungeon):
            response = game_controller_pb2.ServerResponse()
            response.dungeon = pickle.dumps(dungeon)
            response.result = result.value
            logging.info(result)
            return response

        session = self._sessions[request.session_id]
        result = session.make_turn(request.player_id, request.turn)
        return build_response(result, session.dungeon)

    def _set_up_logs(self):
        log_name = 'game_process' + time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + '.log'
        if not os.path.exists(self.LOGS_DIR):
            os.makedirs(self.LOGS_DIR)
        logging.basicConfig(filename=os.path.join(self.LOGS_DIR, log_name), format='%(levelname)s:%(message)s',
                            level=logging.INFO)


def serve(port):
    """
    Running grpc server.
    :param port: a server to run grpc.
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_controller_pb2_grpc.add_GameControllerServicer_to_server(GameControllerServer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
