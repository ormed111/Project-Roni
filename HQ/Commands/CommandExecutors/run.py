from Universal import Command
from Universal import Helper
from Universal.constants import CommandConstants as consts

class RunCommand(Command):
    def __init__(self, command_literal, connection_socket, command_to_run):
        super(RunCommand, self).__init__(command_literal, connection_socket, command_to_run=command_to_run)

    def run(self):
        process_id = self.connection_socket.receive_data(print_progress=False)
        if Helper.is_invalid_message(process_id):
            # run command was invalid..
            Helper.print_and_log(process_id)
        else:
            Helper.print_and_log(consts.RUN_COMMAND_SUCCESSFUL_MSG.format(self.command_to_run, process_id))
