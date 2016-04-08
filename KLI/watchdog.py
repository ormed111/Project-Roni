import os
from subprocess import Popen
from time import sleep

class Script(object):
    _NOT_RUNNING_SCRIPT_DESC = "Script not runnning"
    _RUN_SCRIPT_CLI_COMMAND = "pythonw {}"

    def __init__(self, path):
        self.path = path
        self.is_running = False
        self.process = None
        self.process_id = self._NOT_RUNNING_SCRIPT_DESC

    @property
    def run_command(self):
        return self._RUN_SCRIPT_CLI_COMMAND.format(self.path)

    def run(self):
        if not self.is_running:
            self.process = Popen(self.run_command)
            self.process_id = self.process.pid
            self.is_running = True

    def terminate(self):
        if self.is_running:
            self.process.terminate()
            self.is_running = False
            self.process_id = self._NOT_RUNNING_SCRIPT_DESC

class WatchDog(object):
    _TASKLIST_CLI_COMMAND = 'tasklist /FI "IMAGENAME eq {}*"'

    def __init__(self, iteration_time_period, scripts_paths, scripts_task_name):
        self.iteration_time_period = iteration_time_period
        self.scripts_paths = scripts_paths
        self.scripts_task_name = scripts_task_name
        self._initiate_scripts()
        self.is_running = False

    def _initiate_scripts(self):
        self.scripts = []
        for script_path in self.scripts_paths:
            self.scripts.append(Script(script_path))

    def run(self):
        for script in self.scripts:
            script.run()
        self.is_running = True

    def terminate(self):
        for script in self.scripts:
            script.terminate()
        self.is_running = False

    def _get_tasklist(self):
        tasklist_cli_command = self._TASKLIST_CLI_COMMAND.format(self.scripts_task_name)
        return os.popen(tasklist_cli_command).read()

    def _check_scripts(self):
        if not self.is_running: # watchdog has been commenced yet
            return

        tasklist = self._get_tasklist()
        for script in self.scripts:
            search_str = " {} ".format(script.process_id)
            if search_str not in tasklist:
                script.is_running = False
                script.run()

    def main_loop(self):
        self.run()
        while True:
            self._check_scripts()
            sleep(self.iteration_time_period)

class RoniWatchDog(WatchDog):
    SCRIPTS_NAMES = ["kli.py"]
    SLEEP_PERIOD = 30
    SCRIPTS_TASK = "python"

    def __init__(self):
        scripts_paths = map(self._get_full_script_path, self.SCRIPTS_NAMES)
        super(RoniWatchDog, self).__init__(self.SLEEP_PERIOD, self.scripts_paths, self.SCRIPTS_TASK)

    @staticmethod
    def _get_full_script_path(script_name):
        full_path = os.path.join(os.path.abspath(os.curdir), script_name)
        if not os.path.exists(full_path):
            raise ScriptNotFoundError(script_name)
        return full_path

class ScriptNotFoundError(Exception):
    def __init__(self, script_name):
        self.script_name = script_name
    def __str__(self):
        return "Couldn't find script '{}' in relative path".format(self.script_name)

def main():
    watch_dog = RoniWatchDog()
    watch_dog.main_loop()

if __name__ == "__main__":
    main()

