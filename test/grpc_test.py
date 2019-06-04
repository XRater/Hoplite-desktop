import threading

import grpc

from proto.generated import game_controller_pb2, game_controller_pb2_grpc
from src.server.game_controller_server import serve

PORT = 11239


def test_register_player_2_sessions():
    _run_server()
    stub = _create_stub()
    session1, player_id1, _ = _register_request(stub)
    session2, player_id2, _ = _register_request(stub)
    assert session1 != session2


def test_register_player_common_session():
    _run_server()
    stub = _create_stub()
    session1, player_id1, _ = _register_request(stub, join_existing_session=True)
    session2, player_id2, _ = _register_request(stub, join_existing_session=True)
    assert session1 == session2
    assert player_id1 != player_id2


def _run_server():
    t = threading.Thread(target=serve, args=(PORT,))
    t.setDaemon(True)
    t.start()


def _create_stub():
    channel = grpc.insecure_channel(f'localhost:{PORT}')
    return game_controller_pb2_grpc.GameControllerStub(channel)


def _register_request(stub, join_existing_session=False):
    def create_request():
        request = game_controller_pb2.RegistrationRequest()
        request.join_existing_session = join_existing_session
        return request

    request = create_request()
    response = stub.Register(request)
    return response.session_id, response.player_id, response.dungeon
