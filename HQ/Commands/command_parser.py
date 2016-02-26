from Universal.constants import CommandConstants as consts
from CommandExecutors import *
from Universal import Helper

class CommandParser(object):
    """
        Class of static functions that get command literals and parses them.
        If command_literal is valid, functions will return a tuple where first value is a Sub-Command class
                                     and the second value is a list containing relevant info for command execution.
    """

    @staticmethod
    def getfile_command_parser(getfile_command_literal):
        file_path = getfile_command_literal[len(consts.GETFILE_COMMAND_INDICATOR) + 1:]
        return GetFileCommand,[file_path]

    @staticmethod
    def screenshot_command_parser(screenshot_command_literal):
        args = screenshot_command_literal.split(' ')[1:]
        if len(args) not in consts.SCREENSHOT_VALID_ARGS_COUNT:
            raise TypeError(consts.SCREENSHOT_INVALID_ARGS_ERROR_MSG)
        elif len(args) == 0:
            return ScreenshotCommand, [1, 0]
        else:
            try:
                num_args = map(int, args)
                num_args[1] /= 1000.0 # arg is in ms
                return ScreenshotCommand, num_args
            except ValueError: # args are not numerical
                raise TypeError(consts.SCREENSHOT_INVALID_ARGS_ERROR_MSG)

    @staticmethod
    def kill_kli_command_parser(kill_kli_command_literal):
        return KillKliCommand, []

    @staticmethod
    def run_command_parser(run_command_literal):
        command_to_run = run_command_literal[len(consts.RUN_COMMAND_INDICATOR) + 1:]
        return RunCommand, [command_to_run]

    @staticmethod
    def getdir_command_parser(getdir_command_literal):
        dir_path = getdir_command_literal[len(consts.GETDIR_COMMAND_INDICATOR) + 1:]
        return GetDirCommand, [dir_path]


INDICATOR_PARSER_DICT = {consts.GETFILE_COMMAND_INDICATOR:    CommandParser.getfile_command_parser,
                         consts.SCREENSHOT_COMMAND_INDICATOR: CommandParser.screenshot_command_parser,
                         consts.KILL_KLI_COMMAND_INDICATOR:   CommandParser.kill_kli_command_parser,
                         consts.RUN_COMMAND_INDICATOR:        CommandParser.run_command_parser,
                         consts.GETDIR_COMMAND_INDICATOR:     CommandParser.getdir_command_parser}

def parse_command(command_literal, connection_socket):
    # default command class is of a regular cmd command
    command_class = CmdCommand
    command_args = []

    # search for unique command indicators in command_literal
    for command_indicator, parser_func in INDICATOR_PARSER_DICT.items():
        if command_literal.startswith(command_indicator):
            try:
                command_class, command_args = parser_func(command_literal)
            except TypeError, e: # args were invalid
                Helper.print_and_log(e)
                return

    return command_class(command_literal, connection_socket, *command_args)



