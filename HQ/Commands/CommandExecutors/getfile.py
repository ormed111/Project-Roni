from Universal import Command
from Universal import Helper
from Universal.constants import CommandConstants as consts
import os

class GetFileCommand(Command):
    def __init__(self, command_literal, connection_socket, file_path, products_dir_path=""):
        super(GetFileCommand, self).__init__(command_literal, connection_socket, file_path=file_path,
                                             products_dir_path=products_dir_path)

    def _create_dir_tree(self):
        products_dir = consts.PRODUCTS_DIR.format(hostname=self.connection_socket.peer_hostname,
                                                  ip=self.connection_socket.peer_ip)
        file_dir, file_name = os.path.split(self.file_path.replace(":", ""))
        dir_steps = [''] + file_dir.split(os.path.sep)
        for dir_path in dir_steps:
            products_dir = os.path.join(products_dir, dir_path)
            if not os.path.exists(products_dir):
                os.mkdir(products_dir)
        return os.path.join(products_dir, file_name)

    def run(self):
        # get file data
        file_data = self.connection_socket.receive_data()
        if consts.INVALID_COMMAND_RESPONSE_INDICATOR in file_data:
            # command was invalid..
            Helper.print_and_log(file_data)
            return
        # create dir tree at home for file
        if not self.products_dir_path:
            local_file_path = self._create_dir_tree()
        else:
            local_file_path = os.path.join(self.products_dir_path, os.path.basename(self.file_path))
        # save file
        with open(local_file_path, 'wb') as f:
            f.write(file_data)
        Helper.print_and_log(consts.GETFILE_COMPLETE_MSG.format(self.file_path))



