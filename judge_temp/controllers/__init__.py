"""
This module by default contains some helper functions which
are common to both dbOperations and fileOperations. It also contains
certain methods which require frequent user
"""

import threading
import time
import signal
import os
from subprocess32 import Popen, STDOUT, PIPE


def get_extension_of_file(filename):
    """
        Returns extension of a file in string format

        Args:
            filename(str): name of the file
        Returns:
            str: extension of file
    """
    return filename.rsplit('.', 1)[1]


def mkdir_p(path):
    """
        implements mkdir -p functionality of linux shell in python. It might raise
        error in concurrent conditions
    """
    if not os.path.exists(path):
        os.makedirs(path)


def run_popen_with_timeout(command_string, timeout):
    """
    Run a sub-program in subprocess.Popen, pass it the input_data,
    kill it if the specified timeout has passed.
    returns a tuple of success, stdout, stderr
    """
    kill_check = threading.Event()

    def _kill_process_after_a_timeout(pid):
        os.kill(pid, signal.SIGTERM)
        kill_check.set()  # tell the main routine that we had to kill
        # use SIGKILL if hard to kill...
        return

    p = Popen(command_string, bufsize=1, shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    pid = p.pid
    watchdog = threading.Timer(timeout, _kill_process_after_a_timeout, args=(pid,))
    watchdog.start()
    stdout, stderr = p.communicate()
    watchdog.cancel()  # if it's still waiting to run
    success = not kill_check.isSet()
    kill_check.clear()
    return (success, stdout, stderr)
