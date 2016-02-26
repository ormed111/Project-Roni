from Universal import Command
from Universal import Helper
from Universal.constants import CommandConstants as consts

class KillKliCommand(Command):
    def __init__(self, command_literal, connection_socket):
        super(KillKliCommand, self).__init__(command_literal, connection_socket)

    def run(self):
        Helper.print_and_log(consts.KILLED_KLI_MSG)
        self.connection_socket.terminate_socket()
        return True # this will end keep alive loop