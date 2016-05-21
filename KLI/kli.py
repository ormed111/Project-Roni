from Universal.constants import ConnectionConstants as consts
from Universal import ServerSocketHandler
from Commands import parse_command


class Kli(object):
    def __init__(self):
        self._raise_kli()

    def _raise_kli(self):
        self.connection_socket = ServerSocketHandler(consts.TCP_PORT)

    def run(self):
        keep_alive = None

        while keep_alive is None:
            command_literal = self.connection_socket.receive_command()
            if command_literal is False: # socket has timed-out.. keep waiting
                continue
            command = parse_command(command_literal, self.connection_socket)
            keep_alive = command.run()

