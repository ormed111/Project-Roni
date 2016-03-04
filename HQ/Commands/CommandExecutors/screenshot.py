from ..getter_command import GetterCommand
from Universal import Helper
from Universal.constants import CommandConstants as consts
from Universal.constants import ConnectionConstants
import os

class ScreenshotCommand(GetterCommand):
    def __init__(self, command_literal, connection_socket, products_base_dir, screenshot_count, time_gap):
        super(ScreenshotCommand, self).__init__(command_literal, connection_socket, products_base_dir,
                                                screenshot_count=screenshot_count, time_gap=time_gap)
    def _create_local_path(self):
        screenshots_dir = os.path.join(self._products_base_dir, consts.SCREENSHOTS_DIR_NAME)
        Helper.create_dir_tree(screenshots_dir)
        return screenshots_dir

    def _get_single_screenshot(self):
        # get data
        screenshot_data = self.connection_socket.receive_data()
        screenshot_name = self.connection_socket.receive_data(print_progress=False)
        # save screenshot
        screenshot_path = os.path.join(self.local_path, screenshot_name)
        with open(screenshot_path, 'wb') as screenshot:
            screenshot.write(screenshot_data)
        Helper.print_and_log(consts.SCREENSHOT_COMPLETE_MSG)

    def run(self):
        self.connection_socket.set_timeout_period(None) # so socket doesn't timeout between screenshots
        # get screenshots
        for i in xrange(self.screenshot_count):
            self._get_single_screenshot()
            Helper.print_and_log()

        # return socket timeout
        self.connection_socket.set_timeout_period(ConnectionConstants.SOCKET_TIMEOUT_LENGTH)

