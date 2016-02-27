from Universal import Command
from Universal import Helper
import os

class GetterCommand(Command):
    def __init__(self, command_literal, connection_socket, products_base_dir, **kwargs):
        super(GetterCommand, self).__init__(command_literal, connection_socket, _products_base_dir=products_base_dir,
                                            **kwargs)
        self._create_products_base_dir_tree()

    def _create_products_base_dir_tree(self):
        Helper.create_dir_tree(self._products_base_dir)

    def _create_final_products_dir_tree(self, relative_dir_path):
        """
            Method gets the path of a dir in yaad and creates a product dir for it locally
        """
        relative_dir_path = relative_dir_path.replace(':', '')
        final_products_dir_path = os.path.join(self._products_base_dir, relative_dir_path)
        Helper.create_dir_tree(final_products_dir_path)
        return final_products_dir_path