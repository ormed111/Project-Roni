import os

class Helper(object):

    @staticmethod
    def print_and_log(output=""):
        """
            Implement this..
        """
        print output


    @staticmethod
    def create_dir_tree(dir_path):
        """
            Method gets the path of a directory and creates the dir's tree
        """
        dir_tree_steps = dir_path.split(os.path.sep)
        for i in xrange(len(dir_tree_steps)):
            dir_step_path = os.path.sep.join(dir_tree_steps[: i + 1])
            if not os.path.exists(dir_step_path):
                os.mkdir(dir_step_path)





