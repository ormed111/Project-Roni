import socket
from DataTransmission import DataTransmitter
from Universal.constants import DataTransmissionConstants as consts

class SocketHandler(object):
    def __init__(self, tcp_port, socket_timeout):
        self._socket = socket.socket()
        self.tcp_port = tcp_port
        self._socket_timeout = socket_timeout

    def _init_data_transmitter(self):
        self._data_transmitter = DataTransmitter(self._socket)

    def send_command(self, command_literal):
        return self._data_transmitter.send_command(command_literal)

    def receive_command(self):
        return self._data_transmitter.receive_command()

    def send_data(self, data, print_progress=False):
        return self._data_transmitter.send_raw_data(data, print_progress)

    def receive_data(self, print_progress=True):
        # todo: think what to do with this..
        # socket timeout for no apparent reason sometimes
        #
        # try:
        #     data = DataTransmission.receive_raw_data(self._socket, print_progress)
        # except Exception, e: # any error that may occur..
        #     print "exception raised: {}".format(e) # need to think if keep this or not..
        #     return False

        data = self._data_transmitter.receive_raw_data(print_progress)
        if data is False:
            return consts.SOCKET_TIMEOUT_WHILE_RECEIVING_DATA
        # transmission succeeded
        return data

    def terminate(self):
        self._socket.close()

    def set_timeout_period(self, timeout_period):
        self._socket.settimeout(timeout_period)

class ClientSocketHandler(SocketHandler):
    def __init__(self, tcp_port, peer_hostname, socket_timeout=None):
        super(ClientSocketHandler, self).__init__(tcp_port)
        self.peer_hostname = peer_hostname
        self.peer_ip = socket.gethostbyname(self.peer_hostname)
        self._socket_timeout = socket_timeout
        self._connect_to_server()
        self._init_data_transmitter()

    def _connect_to_server(self):
        """
            Socket is a client that connects to server, Server name is given in "peer_hostname" attribute.
        """
        try:
            self._socket.connect((self.peer_hostname, self.tcp_port))
        except Exception: # socket.getaddrinfo error
            # connection failed
            raise RuntimeError("Connection Failed")
        # set socket timeout
        self._socket.settimeout(self._socket_timeout)

class ServerSocketHandler(SocketHandler):
    def __init__(self, tcp_port, socket_timeout=None):
        super(ServerSocketHandler, self).__init__(tcp_port, socket_timeout)
        self._raise_server()
        self._init_data_transmitter()

    def _raise_server(self):
        """
            Socket is a server that waits for a client connection.
        """
        self._socket.bind(('', self.tcp_port))
        self._socket.listen(1)
        # wait for connection from client`
        conn, address = self._socket.accept()
        # close socket in favor of connection socket
        self._socket.close()
        self._socket = conn
        # get additional peer info
        self.peer_ip = address[0]
        self.peer_hostname = socket.gethostbyaddr(self.peer_ip)

