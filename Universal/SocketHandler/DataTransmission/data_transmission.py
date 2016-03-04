from Universal.constants import DataTransmissionConstants as consts
from crypto import Crypto
from Universal.helper import Helper

class DataTransmitter(object):
    def __init__(self, connection_socket):
        self.connection_socket = connection_socket

    ############ DATA SENDING

    def _send_data_by_protocol(self, data):
        """
            Protocol is that after any data is sent, an ack must be received
        """
        data = str(data) # must be a string
        self.connection_socket.sendall(data)
        # wait for ack
        # first, receive response
        try:
            command_response = self.connection_socket.recv(consts.RECV_BUFFER_SIZE)
        except Exception: # socket.timeout
            return False
        # second, check if it is an ack
        if command_response == consts.ACK:
            return True
        else:
            print command_response
            raise ValueError(consts.UNKNOWN_COMMAND_RESPONSE_ERROR_MSG)

    def send_command(self, command_literal):
        return self._send_data_by_protocol(command_literal)

    def send_raw_data(self, data):
        data = Crypto.encrypt_data(data)
        data_size = len(data)
        # inform other side of incoming data size
        if not self._send_data_by_protocol(data_size):
             return False # data size failed
        # send data
        for i in xrange(0, data_size, consts.MAX_SENT_DATA_SIZE):
            data_chunk = data[i: i + consts.MAX_SENT_DATA_SIZE]
            self._send_data_by_protocol(data_chunk)
        return True

    ############ DATA RECEIVING

    def _receive_data_by_protocol(self, buffer_size=consts.RECV_BUFFER_SIZE):
        """
            Protocol is that after any data is received, an ack must be sent
        """
        received_data = self.connection_socket.recv(buffer_size)
        self.connection_socket.sendall(consts.ACK) # send ack
        return received_data

    def receive_command(self):
        return self._receive_data_by_protocol()

    def receive_raw_data(self, print_progress=True):
        # get size of incoming data
        data_size = int(self._receive_data_by_protocol())
        # get data
        data = ""
        prev_percent = 0
        while len(data) < data_size:
            data += self._receive_data_by_protocol(buffer_size=consts.MAX_SENT_DATA_SIZE)
            # print progress of data transfer
            if print_progress:
                progress_percent = (len(data) / float(data_size)) * 100
                if progress_percent > prev_percent + 10:
                    prev_percent = progress_percent
                    Helper.print_and_log("progress: {}%".format(progress_percent))
        return Crypto.decrypt_data(data)