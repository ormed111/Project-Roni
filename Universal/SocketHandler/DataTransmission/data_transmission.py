from functools import wraps
from Universal.constants import DataTransmissionConstants as consts
from crypto import Crypto
from Universal.helper import Helper
from socket import timeout as SocketTimeoutException


def _transmit_data_and_catch_socket_exceptions(data_transmission_func):
    """
        Wrapper catches and handles any socket module exception that may occur during data transmission
    """
    @wraps(data_transmission_func)
    def transmit_data_and_catch(*args, **kwargs):
        try:
            return data_transmission_func(*args, **kwargs)
        except SocketTimeoutException:
            return False
    return transmit_data_and_catch


class DataTransmitter(object):
    def __init__(self, connection_socket):
        self.connection_socket = connection_socket

    ############ UNIVERSAL

    @staticmethod
    def _print_transmission_progress_percent(total_data_size, received_data_size, progress_percent):
        current_progress_percent = (float(received_data_size) / total_data_size) * 100
        if current_progress_percent > progress_percent + 10:
            Helper.print_and_log("progress: {}%".format(current_progress_percent))
            return current_progress_percent
        return progress_percent

    ############ DATA SENDING

    def _send_data_by_protocol(self, data):
        """
            Protocol is that after any data is sent, an ack must be received
        """
        data = str(data) # must be a string
        self.connection_socket.sendall(data)
        # wait for ack
        # first, receive response
        command_response = self.connection_socket.recv(consts.RECV_BUFFER_SIZE)
            # try:
            #     command_response = self.connection_socket.recv(consts.RECV_BUFFER_SIZE)
            # except SocketTimeoutException:
            #     return False
        # second, check if it is an ack
        if command_response != consts.ACK:
            print command_response
            raise ValueError(consts.UNKNOWN_COMMAND_RESPONSE_ERROR_MSG)

    @_transmit_data_and_catch_socket_exceptions
    def send_command(self, command_literal):
        self._send_data_by_protocol(command_literal)
        return True

    @_transmit_data_and_catch_socket_exceptions
    def send_raw_data(self, data, print_progress):
        data = Crypto.encrypt_data(data)
        data_size = len(data)
        # inform other side of incoming data size
        self._send_data_by_protocol(data_size)
            # if not self._send_data_by_protocol(data_size):
            #      return False # data size failed
        # send data
        progress_percent = 0
        for i in xrange(0, data_size, consts.MAX_SENT_DATA_SIZE):
            data_chunk = data[i: i + consts.MAX_SENT_DATA_SIZE]
            self._send_data_by_protocol(data_chunk)
            if print_progress:
                # print progress of data transfer
                sent_data_size = data_size if i + consts.MAX_SENT_DATA_SIZE > data_size else i + consts.MAX_SENT_DATA_SIZE # if all data has been sent..
                progress_percent = self._print_transmission_progress_percent(data_size, sent_data_size, progress_percent)
        return True

    ############ DATA RECEIVING

    def _receive_data_by_protocol(self, buffer_size=consts.RECV_BUFFER_SIZE):
        """
            Protocol is that after any data is received, an ack must be sent
        """
        received_data = self.connection_socket.recv(buffer_size)
        self.connection_socket.sendall(consts.ACK) # send ack
        return received_data

    @_transmit_data_and_catch_socket_exceptions
    def receive_command(self):
        return self._receive_data_by_protocol()

    @_transmit_data_and_catch_socket_exceptions
    def receive_raw_data(self, print_progress):
        # get size of incoming data
        data_size = int(self._receive_data_by_protocol())
        # get data
        data = ""
        progress_percent = 0
        while len(data) < data_size:
            data += self._receive_data_by_protocol(buffer_size=consts.MAX_SENT_DATA_SIZE)
            if progress_percent:
                # print progress of data transfer
                progress_percent = self._print_transmission_progress_percent(data_size, len(data), progress_percent)
        return Crypto.decrypt_data(data)
