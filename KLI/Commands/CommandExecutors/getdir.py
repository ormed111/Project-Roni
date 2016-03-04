from Universal import Command
from Universal.constants import CommandConstants as consts
import os
from glob import glob
from pickle import dumps
from getfile import GetFileCommand


class GetDirCommand(Command):
    def __init__(self, command_literal, connection_socket, dir_path):
        super(GetDirCommand, self).__init__(command_literal, connection_socket, dir_path=dir_path)

    def _get_items_info(self):
        """
            Method gets information regarding items in directory and saves it as attributes of class.
            Saves two things: 1. A dictionary of file paths in directory and their sizes.
                              2. A list of sub directories in directory.
        """
        # get all items in directory
        items = glob(os.path.join(self.dir_path, '*'))
        # create file paths and sizes dict
        self.file_sizes = {file_path: os.path.getsize(file_path) for file_path in filter(os.path.isfile, items)}
        # create sub dirs list
        self.sub_dirs = [os.path.basename(sub_dir_path) for sub_dir_path in filter(os.path.isdir, items)]

    def _confirm_command_execution(self):
        # get info on items (files and sub dirs) in directory
        self._get_items_info()
        # send info objects to hq
        dir_info_data = dumps((self.file_sizes, self.sub_dirs))
        self.connection_socket.send_data(dir_info_data)
        # receive confirmation from hq
        confirmation = self.connection_socket.receive_data(print_progress=False)
        return confirmation.lower() == consts.GETDIR_POSITIVE_CONFIRMATION

    def _send_files(self):
        for file_path in self.file_sizes.keys():
            # send file path to hq
            self.connection_socket.send_data(file_path)
            # send data
            getfile_command = GetFileCommand(self.command_literal, self.connection_socket, file_path)
            getfile_command.run()

    def run(self):
        # check if dir exists
        if not os.path.isdir(self.dir_path):
            self.connection_socket.send_data(consts.GETDIR_DIR_PATH_INVALID_MSG.format(self.dir_path))
            return
        # get continue confirmation from hq
        if not self._confirm_command_execution():
            return
        # send files data
        self._send_files()








