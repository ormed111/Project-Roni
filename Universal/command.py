"""
    Generic HQ command class
"""

class Command(object):
    def __init__(self, command_literal, connection_socket, **kwargs):
        self.command_literal = command_literal
        self.connection_socket = connection_socket
        for key, val in kwargs.items():
            setattr(self, key, val)

    def run(self):
        raise NotImplementedError("Override me!")
