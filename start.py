import argparse

from src.app_controller.app_controller import AppController
from src.server.game_controller_server import serve

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('-s', '--server', action="store_true", default=False, help='Pass it if you want to start server')
    arg('--host', type=str, help='Ip address of host')
    arg('-p', '--port', default=10239, type=int, help='Port of host')
    args = parser.parse_args()

    if args.server:
        serve(args.port)
    elif args.host:
        controller = AppController()
        controller.start(args.host, args.port)
    else:
        parser.print_help()
