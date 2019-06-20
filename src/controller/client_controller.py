import logging
import pickle

import grpc

from proto.generated import game_controller_pb2_grpc, game_controller_pb2
from src.controller.direction import Direction
from src.controller.equipment_command import EquipmentCommand
from src.controller.move_command import MoveCommand
from src.controller.turn_result import TurnResult


class ClientController(object):
    """It's a class that plays role of `C` in a standard MVC pattern."""

    def __init__(self, view, host, port):
        self._host = host
        self._port = port
        self._view = view
        self._session = None
        self._player_id = None

        self._view.get_turn()
        channel = grpc.insecure_channel(f'{self._host}:{self._port}')
        self._stub = game_controller_pb2_grpc.GameControllerStub(channel)

    def process_user_command(self, command):
        """
        This is a very important method that sends user request to server. The request is asynchronous.
        All actions except QUIT will be blocked until response from server.
        :param command: a command to execute.
        :return: None
        """
        self._view.block_input()

        def callback(future):
            result, dungeon = parse_response(future.result())
            if result == TurnResult.TURN_ACCEPTED.value:
                logging.info("Turn was accepted. Waiting for new turn")
                self._view.render_dungeon(dungeon)
                self._view.get_turn()
            if result == TurnResult.GAME_OVER.value:
                logging.info("Game over")
                self._view.game_over()
            if result == TurnResult.BAD_TURN.value:
                logging.info("Turn was not valid")
                self._view.render_dungeon(dungeon)
                self._view.get_turn()

        def create_request():
            request = game_controller_pb2.ClientRequest()
            request.session_id = self._session
            request.player_id = self._player_id

            if isinstance(command, MoveCommand):
                if command.direction == Direction.DOWN:
                    request.turn.move = game_controller_pb2.DOWN
                elif command.direction == Direction.UP:
                    request.turn.move = game_controller_pb2.UP
                elif command.direction == Direction.LEFT:
                    request.turn.move = game_controller_pb2.LEFT
                elif command.direction == Direction.RIGHT:
                    request.turn.move = game_controller_pb2.RIGHT

            request.turn.equipment_item = -1
            if isinstance(command, EquipmentCommand):
                request.turn.equipment_item = command.item

            return request

        def parse_response(response):
            return response.result, pickle.loads(response.dungeon)

        request = create_request()
        future = self._stub.MakeTurn.future(request)
        future.add_done_callback(callback)

    def save_game(self, filename):
        """
        Saving current to the file.
        :param filename: filename to use
        """
        logging.info('Saving game to {}'.format(filename))
        with open(filename, 'wb') as file:
            pickle.dump(self._dungeon.field, file)

    def register(self, join_existing_session=False):
        """
        A method to inform a server about new player.
        :param join_existing_session: True if want to join a random existing session.
        :return: our player id, dungeon
        """

        def create_request():
            request = game_controller_pb2.RegistrationRequest()
            request.join_existing_session = join_existing_session
            return request

        def parse_response(response):
            self._session = response.session_id
            self._player_id = response.player_id
            return pickle.loads(response.dungeon)

        request = create_request()
        dungeon = parse_response(self._stub.Register(request))
        return self._player_id, dungeon
