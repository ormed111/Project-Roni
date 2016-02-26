from Universal.constants import ConnectionConstants as consts
from Universal import SocketHandler
from Commands import parse_command


class Kli(object):
    def __init__(self):
        self._raise_kli()

    def _raise_kli(self):
        self.connection_socket = SocketHandler(server=True, tcp_port=consts.TCP_PORT)

    def run(self):
        keep_alive = None

        while keep_alive is None:
            command_literal = self.connection_socket.receive_command()
            command = parse_command(command_literal, self.connection_socket)
            keep_alive = command.run()

