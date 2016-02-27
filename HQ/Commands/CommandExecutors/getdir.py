from ..getter_command import GetterCommand
from Universal import Helper
from Universal.constants import CommandConstants as consts
from pickle import loads
import os
from getfile import GetFileCommand

class GetDirCommand(GetterCommand):
    def __init__(self, command_literal, connection_socket, products_base_dir, dir_path):
        super(GetDirCommand, self).__init__(command_literal, connection_socket, products_base_dir, dir_path=dir_path)

    def _create_local_path(self):
        return self._create_final_products_dir_tree(self.dir_path)

    def _confirm_command_execution(self):
        """
            Method calculates the size of data to be transmitted, and confirms with user
            that execution is to continue
        """
        total_file_size = sum(self.file_sizes.values()) / 1000.0
        confirmation = raw_input(consts.GETDIR_CONFIRMATION_MSG.format(total_file_size),)
        self.connection_socket.send_data(confirmation)
        return confirmation.lower() == consts.GETDIR_POSITIVE_CONFIRMATION

    def _get_files(self):
        for i in xrange(len(self.file_sizes)):
            # get file path from kli
            file_path = self.connection_socket.receive_data()
            # get file data
            getfile_command = GetFileCommand(self.command_literal, self.connection_socket, self._products_base_dir,
                                             file_path, self.local_path)
            getfile_command.run()
            Helper.print_and_log()

    def _create_sub_dirs(self):
        for sub_dir_name in self.sub_dirs:
            local_sub_dir_path = os.path.join(self.local_path, sub_dir_name)
            if not os.path.exists(local_sub_dir_path):
                os.mkdir(local_sub_dir_path)

    def run(self):
        dir_item_info = self.connection_socket.receive_data(print_progress=False)
        if consts.INVALID_COMMAND_RESPONSE_INDICATOR in dir_item_info:
            # dir path was invalid..
            Helper.print_and_log(dir_item_info)
            return

        # get all file and dir paths in directory as dictionary
        self.file_sizes, self.sub_dirs = loads(dir_item_info)
        # get user continue execution confirmation
        if self._confirm_command_execution():
            # get all files in directory
            self._get_files()
            # create empty sub directories in Product dir
            self._create_sub_dirs()



