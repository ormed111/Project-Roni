from Universal.constants import DataTransmissionConstants as consts
from crypto import Crypto
from Universal.helper import Helper

class DataTransmission(object):

    ############ DATA SENDING

    @classmethod
    def send_command(cls, command_literal, connection_socket):
        connection_socket.sendall(command_literal)
        # wait for ack
        # first, receive response
        try:
            command_response = connection_socket.recv(consts.RECV_BUFFER_SIZE)
        except Exception: # socket.timeout
            return False
        # second, check if it is an ack
        if command_response == consts.ACK:
            return True
        else:
            print command_response
            raise ValueError(consts.UNKNOWN_COMMAND_RESPONSE_ERROR_MSG)

    @classmethod
    def send_raw_data(cls, data, connection_socket):
        data = Crypto.encrypt_data(data)
        data_size = len(data)
        # inform other side of incoming data size
        connection_socket.sendall(str(data_size))
        connection_socket.recv(consts.RECV_BUFFER_SIZE) # wait for ack..
        # sent data
        for i in xrange(0, data_size, consts.MAX_SENT_DATA_SIZE):
            connection_socket.sendall(data[i: i + consts.MAX_SENT_DATA_SIZE])
            connection_socket.recv(consts.RECV_BUFFER_SIZE) # wait for ack..


    ############ DATA RECEIVING

    @classmethod
    def receive_command(cls, connection_socket):
        command_literal = connection_socket.recv(consts.RECV_BUFFER_SIZE)
        connection_socket.sendall(consts.ACK)
        return command_literal

    @classmethod
    def receive_raw_data(cls, connection_socket, print_progress=True):
        # get size of incoming data
        data_size = int(connection_socket.recv(consts.RECV_BUFFER_SIZE))
        connection_socket.sendall(consts.ACK) # send ack
        # get data
        data = ""
        prev_percent = 0
        while len(data) < data_size:
            data += connection_socket.recv(consts.MAX_SENT_DATA_SIZE)
            # print progress of data transfer
            if print_progress:
                progress_percent = (len(data) / float(data_size)) * 100
                if progress_percent > prev_percent + 10:
                    prev_percent = progress_percent
                    Helper.print_and_log("progress: {}%".format(progress_percent))
            connection_socket.sendall(consts.ACK) # send ack
        return Crypto.decrypt_data(data)