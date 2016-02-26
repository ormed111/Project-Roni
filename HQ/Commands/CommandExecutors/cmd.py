from Universal import Command
from Universal.constants import CommandConstants as consts
from Universal import Helper

class CmdCommand(Command):
    def __init__(self, command_literal, connection_socket):
        super(CmdCommand, self).__init__(command_literal, connection_socket)

    def run(self):
        # get file data
        output = self.connection_socket.receive_data(print_progress=False)
        Helper.print_and_log()
        Helper.print_and_log(output)




