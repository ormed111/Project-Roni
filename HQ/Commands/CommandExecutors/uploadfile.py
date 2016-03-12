from Universal import Command, Helper
from Universal.constants import CommandConstants as consts
import os

class UploadFileCommand(Command):
    def __init__(self, command_literal, connection_socket, file_to_send_path):
        super(UploadFileCommand, self).__init__(command_literal, connection_socket, file_to_send_path=file_to_send_path)

    def _file_to_send_exists(self):
        return os.path.isfile(self.file_to_send_path)

    def _send_file_name(self):
        file_name = os.path.basename(self.file_to_send_path)
        return self.connection_socket.send_data(file_name)

    def _send_file(self):
        # send file name
        send_status = self._send_file_name()
        if not send_status:
            return False

        # send file data
        with open(self.file_to_send_path, 'rb') as file_obj:
            file_data = file_obj.read()
        send_status = self.connection_socket.send_data(file_data, print_progress=True)
        return send_status

    def run(self):
        # determine if file to send exists
        if not self._file_to_send_exists():
            Helper.print_and_log(consts.UPLOAD_FILE_DOESNT_EXIST_MSG.format(self.file_to_send_path))
            return
        # send the data of the file to dst
        if not self._send_file():
            Helper.print_and_log(consts.UPLOAD_FILE_SEND_FAILED_MSG.format(self.file_to_send_path))
            return
        # print the final status of command received from kli
        kli_msg = self.connection_socket.receive_data(print_progress=False)
        Helper.print_and_log(kli_msg)

