from Universal import Command
from Universal.constants import CommandConstants as consts
import subprocess

class RunCommand(Command):
    def __init__(self, command_literal, connection_socket, command_to_run):
        super(RunCommand, self).__init__(command_literal, connection_socket, command_to_run=command_to_run)

    def run(self):
        """
            Run the command given using subprocess module.
        """
        try:
            process = subprocess.Popen(self.command_to_run)
            pid = str(process.pid)
            self.connection_socket.send_data(pid)
        except WindowsError:
            error_msg = consts.RUN_COMMAND_INVALID.format(self.command_to_run)
            self.connection_socket.send_data(error_msg)