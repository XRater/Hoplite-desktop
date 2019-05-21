import logging
import pickle
from multiprocessing.pool import Pool

import grpc

from proto.generated import game_controller_pb2_grpc, game_controller_pb2
from src.controller.turn_result import TurnResult


class ClientController(object):
    """It's a class that plays role of `C` in a standard MVC pattern."""

    def __init__(self, view, host, port):
        self.pool = Pool(processes=1)
        self._host = host
        self._port = port
        self._view = view
        self._stub = None
        # logging.info('Dungeon is completed')

    def start(self):
        # initialize
        # self._view.render_dungeon(self._dungeon)
        self._view.get_turn()
        channel = grpc.insecure_channel(f'{self._host}:{self._port}')
        self._stub = game_controller_pb2_grpc.GameControllerStub(channel)

    def process_user_command(self, command):
        self._view.block_input()

        def callback(result):
            raise ValueError(result)
            dungeon = result
            self._dungeon = dungeon
            if result == TurnResult.TURN_ACCEPTED:
                logging.info("Turn was accepted. Waiting for new turn")
                self._view.render_dungeon(self._dungeon)
                self.call_enemy_turn()
            if result == TurnResult.GAME_OVER:
                logging.info("Game over")
                self._view.game_over()
            if result == TurnResult.BAD_TURN:
                logging.info("Turn was not valid")
                self._view.get_turn()

        def create_request():
            request = game_controller_pb2.ClientRequest()
            request.turn.move = game_controller_pb2.UP
            request.player_id = 1
            return request

        request = create_request()
        field = self._stub.MakeTurn(request)
        print(field.new_field.height, field.new_field.width)
        # self.pool.apply_async(self._stub.MakeTurn, [request], callback=callback)

    def call_enemy_turn(self):
        result = self._logic.make_turn()
        if result == TurnResult.TURN_ACCEPTED:
            self._view.render_dungeon(self._dungeon)
            self._view.get_turn()
        if result == TurnResult.GAME_OVER:
            logging.info("Game over")
            self._view.game_over()
        if result == TurnResult.BAD_TURN:
            raise Exception()

    def save_game(self, filename):
        logging.info('Saving game to {}'.format(filename))
        with open(filename, 'wb') as file:
            pickle.dump(self._dungeon.field, file)

    def save(self):
        pass
