from ..getter_command import GetterCommand
from Universal import Helper
from Universal.constants import CommandConstants as consts
import os

class GetFileCommand(GetterCommand):
    def __init__(self, command_literal, connection_socket, products_base_dir, file_path, product_final_dir_path=""):
        super(GetFileCommand, self).__init__(command_literal, connection_socket, products_base_dir, file_path=file_path,
                                             _product_final_dir_path=product_final_dir_path)
        self._local_product_path = None

    def _create_file_dir_tree(self):
        """
            Create a local path for file if one was not given on instance creation
        """
        if not self._product_final_dir_path:
            relative_dir_path_of_file = os.path.dirname(self.file_path)
            self._product_final_dir_path = self._create_final_products_dir_tree(relative_dir_path_of_file)
        # format the file path
        file_name = os.path.basename(self.file_path)
        return os.path.join(self._product_final_dir_path, file_name)

    @property
    def local_product_path(self):
        """
            The local path in which the file got from kli will be saved
        """
        if not self._local_product_path:
            self._local_product_path = self._create_file_dir_tree()
        return self._local_product_path

    def run(self):
        # get file data
        file_data = self.connection_socket.receive_data()
        if consts.INVALID_COMMAND_RESPONSE_INDICATOR in file_data:
            # command was invalid.. file_data received was an error message from kli
            Helper.print_and_log(file_data)
            return
        # save file
        with open(self.local_product_path, 'wb') as local_file:
            local_file.write(file_data)
        Helper.print_and_log(consts.GETFILE_COMPLETE_MSG.format(self.file_path))

