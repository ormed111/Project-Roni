from Universal.constants import CommandConstants as consts
from CommandExecutors import *
from Universal import Helper

class CommandParser(object):
    """
        If command_literal is valid, parser_functions will return a tuple where first value is a Sub-Command class
            and the second value is a list containing relevant info for command execution.
    """
    def __init__(self, products_base_dir, connection_socket):
        self._products_base_dir = products_base_dir
        self._connection_socket = connection_socket
        self._indicator_parser_mapping_dict = None

    def _getfile_command_parser(self):
        file_path = self.command_literal[len(consts.GETFILE_COMMAND_INDICATOR) + 1:]
        return GetFileCommand, [self._products_base_dir, file_path]

    def _screenshot_command_parser(self):
        args = self.command_literal.split(' ')[1:]
        if len(args) not in consts.SCREENSHOT_VALID_ARGS_COUNT:
            raise TypeError(consts.SCREENSHOT_INVALID_ARGS_ERROR_MSG)
        elif len(args) == 0:
            num_args = [1, 0]
        else:
            try:
                num_args = map(int, args)
                num_args[1] /= 1000.0 # arg is in ms
            except ValueError: # args are not numerical
                raise TypeError(consts.SCREENSHOT_INVALID_ARGS_ERROR_MSG)

        return ScreenshotCommand, [self._products_base_dir] + num_args

    def _kill_kli_command_parser(self):
        return KillKliCommand, []

    def _run_command_parser(self):
        command_to_run = self.command_literal[len(consts.RUN_COMMAND_INDICATOR) + 1:]
        return RunCommand, [command_to_run]

    def _getdir_command_parser(self):
        dir_path = self.command_literal[len(consts.GETDIR_COMMAND_INDICATOR) + 1:]
        return GetDirCommand, [self._products_base_dir, dir_path]

    def _upload_file_command_parser(self):
        pass

    def _cmd_command_parser(self):
        return CmdCommand, []

    @property
    def _indicator_parser_dict(self):
        if not self._indicator_parser_mapping_dict:
            self._indicator_parser_mapping_dict = {consts.GETFILE_COMMAND_INDICATOR:     self._getfile_command_parser,
                                                   consts.SCREENSHOT_COMMAND_INDICATOR:  self._screenshot_command_parser,
                                                   consts.KILL_KLI_COMMAND_INDICATOR:    self._kill_kli_command_parser,
                                                   consts.RUN_COMMAND_INDICATOR:         self._run_command_parser,
                                                   consts.GETDIR_COMMAND_INDICATOR:      self._getdir_command_parser,
                                                   consts.UPLOAD_FILE_COMMAND_INDICATOR: self._upload_file_command_parser}
        return self._indicator_parser_mapping_dict

    def parse_command(self, command_literal):
        self.command_literal = command_literal

        # default command is a regular windows cmd command
        command_class, command_args = self._cmd_command_parser()

        for command_indicator, parser_func in self._indicator_parser_dict.items():
            # if command has a special command indicator, the literal will be parsed in a proper manner
            if self.command_literal.startswith(command_indicator):
                try:
                    command_class, command_args = parser_func()
                except TypeError, e:
                    Helper.print_and_log(e)
                    return

        return command_class(self.command_literal, self._connection_socket, *command_args)
