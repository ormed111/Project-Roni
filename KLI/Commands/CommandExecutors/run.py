from Universal import Command
from Universal.constants import CommandConstants as consts
import subprocess

class RunCommand(Command):
    def __init__(self, command_literal, connection_socket, command_to_run):
        super(RunCommand, self).__init__(command_literal, connection_socket, command_to_run=command_to_run)

    def _execute_command(self):
        try:
            process = subprocess.Popen(self.command_to_run)
            return_val = str(process.pid)
        except WindowsError:
            return_val = consts.RUN_COMMAND_INVALID.format(self.command_to_run)
        return return_val

    def run(self):
        """
            Run the command given using subprocess module.
            If successful, it returns to hq to process id of the command executed. If not, it return an error message
        """
        self.connection_socket.send_data(self._execute_command())