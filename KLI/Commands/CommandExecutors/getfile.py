import os
from Universal import Command
from Universal.constants import CommandConstants as consts

class GetFileCommand(Command):
    def __init__(self, command_literal, connection_socket, file_path):
        super(GetFileCommand, self).__init__(command_literal, connection_socket, file_path=file_path)

    def run(self):
        # check if file exists
        if not os.path.isfile(self.file_path):
            self.connection_socket.send_data(consts.GETFILE_FILE_PATH_INVALID_MSG.format(self.file_path))
            return
        # file exists - sending data..
        with open(self.file_path, 'rb') as f:
            file_data = f.read()
        self.connection_socket.send_data(file_data)


