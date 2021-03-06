from Universal import Command
from Universal import Helper
import os

class GetterCommand(Command):
    def __init__(self, command_literal, connection_socket, products_base_dir, **kwargs):
        super(GetterCommand, self).__init__(command_literal, connection_socket, _products_base_dir=products_base_dir,
                                            **kwargs)
        self._create_products_base_dir_tree()
        self._local_path = None

    def _create_products_base_dir_tree(self):
        """
            Method creates the base dir in which products will be saved.
        """
        Helper.create_dir_tree(self._products_base_dir)

    def _create_final_products_dir_tree(self, relative_dir_path):
        """
            Method gets the path of a dir in yaad and creates a product dir for it locally
        """
        relative_dir_path = relative_dir_path.replace(':', '')
        final_products_dir_path = os.path.join(self._products_base_dir, relative_dir_path)
        Helper.create_dir_tree(final_products_dir_path)
        return final_products_dir_path

    def _create_local_path(self):
        raise NotImplementedError("Override me!")

    @property
    def local_path(self):
        """
            The path in which the gotten files will be saved, depending on the type of command.
            E.g - for GetFile, the local_path will be where the file is saved
                - for GetDir, the local_path is the dir where the files in the dir will be saved
        """
        if not self._local_path:
            self._local_path = self._create_local_path()
        return self._local_path
