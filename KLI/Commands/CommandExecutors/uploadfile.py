from Universal import Command, Helper
from Universal.constants import CommandConstants as consts
import os

class UploadFileCommand(Command):
    def __init__(self, command_literal, connection_socket, dir_path_to_save_file):
        super(UploadFileCommand, self).__init__(command_literal, connection_socket, dir_path_to_save_file=dir_path_to_save_file)

    def _receive_file_name(self):
        file_name = self.connection_socket.receive_data(print_progress=False)
        self._file_to_save_path = os.path.join(self.dir_path_to_save_file, file_name)

    def _receive_file(self):
        self._receive_file_name()
        # receive file data
        file_data = self.connection_socket.receive_data(print_progress=False)
        return file_data

    def _save_file(self, file_data):
        Helper.create_dir_tree(self.dir_path_to_save_file)
        with open(self._file_to_save_path, 'wb') as file_obj:
            file_obj.write(file_data)

    def _save_file_and_return_msg(self, file_data):
        try:
            self._save_file(file_data)
            msg = consts.UPLOAD_FILE_FINISHED_SUCCESSFULLY.format(self._file_to_save_path)
        except Exception, e:
            msg = consts.UPLOAD_FILE_FAILED_TO_SAVE_FILE.format(self._file_to_save_path, e)
        return msg

    def run(self):
        file_data = self._receive_file()
        msg = self._save_file_and_return_msg(file_data)
        self.connection_socket.send_data(msg)
