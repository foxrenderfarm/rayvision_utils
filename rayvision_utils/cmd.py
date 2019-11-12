"""Process the cmd command and execute it."""

# Import built-in modules
import logging
import os
import subprocess
import sys


# Import local modules
from rayvision_utils.utils import str2unicode
from rayvision_utils.utils import VERSION


# pylint: disable=useless-object-inheritance
class Cmd(object):
    """Execute the cmd command."""

    def run(self, cmd, shell=False, log_output=True):
        """Execute the cmd command to print the output information of cmd.

        Args:
            cmd (str): Cmd command.
            shell (bool): Accept a string type variable as a command and call
                the shell to execute the string, default is False.
            log_output (bool): Whether to output to the console, default is
                True.

        Returns:
            tuple: Status code of the cmd command, output information, error
                message.
                e.g.:
                    (0, 'fd3sa1fa2fsa', 'f51551d5')

        """
        log = logging.getLogger(__name__).info

        log("run command:\n%s", cmd)
        cmd = self.compatible(cmd)
        res_data = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, shell=shell)
        stdout, stderr = res_data.communicate()
        stdout = str2unicode(stdout)
        stderr = str2unicode(stderr)

        if log_output is True:
            log("stdout:\n")
            log(stdout)
        if stderr:
            log("stderr:\n")
            log(stderr)
        return res_data.returncode, stdout, stderr

    @staticmethod
    def power_run(cmd):
        """Pass."""

    @staticmethod
    def wrap_subprocess(cmd):
        """Wrap the child process to execute the cmd command.

        It is convenient to modify subprocess when packaging scripts into exe
        formmat.

        Args:
            cmd (str): Cmd command.

        Returns:
            object: The object obtained by executing the cmd command.

        """
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True,
                                  startupinfo=startupinfo)
        return result

    @staticmethod
    def compatible(cmd):
        """When Python2, the encoding of the cmd command is processed.

        Args:
            cmd (str): Cmd command.

        Returns:
            str: Handled cmd command.

        """
        if VERSION != 3:
            cmd = str(cmd)
            cmd = cmd.encode(sys.getfilesystemencoding())

        return cmd
