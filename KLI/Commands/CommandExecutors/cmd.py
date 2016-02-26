import os
from Universal import Command

class CmdCommand(Command):
    def __init__(self, command_literal, connection_socket):
        super(CmdCommand, self).__init__(command_literal, connection_socket)

    def run(self):
        # get command
        output = os.popen(self.command_literal).read()
        self.connection_socket.send_data(output)