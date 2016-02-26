import socket
from DataTransmission import DataTransmission
from Universal.constants import SocketHandlerConstants as consts


class SocketHandler(object):
    def __init__(self, **kwargs):
        """
            Initiates a SocketHandler of either a client or server socket.
            For a client, kwargs must contains keys:
                @ param client: flag to indicate if socket is of a client
                @ type client: bool
                @ param connect_to: hostname of server to connect to
                @ type connect_to: str
                @ param tcp_port: the tcp port for socket connection
                @ type tcp_port: int
                @ param socket_timeout: number of seconds for socket connection timeout
                @ type socket_timeout: int

            For a server, kwargs must contain keys:
                @ param server: flag to indicate if socket is of a server
                @ type server: bool
                @ param tcp_port: the tcp port for socket connection
                @ type tcp_port: int

        """
        self._socket = socket.socket()
        self.tcp_port = kwargs[consts.TCP_PORT_KEY]

        if consts.CLIENT_KEY in kwargs:
            self.peer_hostname = kwargs[consts.HOSTNAME_KEY]
            self._socket_timeout = kwargs[consts.SOCKET_TIMEOUT_KEY]
            self._connect_to_server()
        elif consts.SERVER_KEY in kwargs:
            self._raise_server()
        else:
            raise TypeError(consts.HANDLER_INITIATE_ERROR_MSG)

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
        # get additional peer info
        self.peer_ip = socket.gethostbyname(self.peer_hostname)

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

    def send_command(self, command_literal):
        return DataTransmission.send_command(command_literal, self._socket)

    def receive_command(self):
        return DataTransmission.receive_command(self._socket)

    def send_data(self, data):
        try:
            DataTransmission.send_raw_data(data, self._socket)
        except Exception: # any error that may occur..
            return False
        # transmission succeeded
        return True

    def receive_data(self, print_progress=True):
        try:
            data = DataTransmission.receive_raw_data(self._socket, print_progress)
        except Exception, e: # any error that may occur..
            print "exception raised: {}".format(e) # need to think if keep this or not..
            return False
        # transmission succeeded
        return data

    def terminate_socket(self):
        self._socket.close()

    def set_timeout_period(self, timeout_period):
        self._socket.settimeout(timeout_period)