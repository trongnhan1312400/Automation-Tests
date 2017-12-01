"""
Created on Nov 22, 2017

@author: nhan.nguyen

Containing classes to catch the log on console and write it file.
"""

import sys
import os
import time
import errno
import logging
import tempfile
import io
from .result import Status
from .constant import Colors


class Printer(object):
    """
    Class that write content to several file.
    Use this class when you want to write log not only on console but only on some other files.
    """
    def __init__(self, *files):
        self.files = files

    def write(self, content):
        """
        Write a content into several files.
        :param content: (optional) content you want to write.
        """
        for f in self.files:
            f.write(content)
            f.flush()  # Want this content is displayed immediately on file

    def flush(self):
        """
        Make the content in buffer display immediately on files.
        """
        for f in self.files:
            f.flush()


class Logger:
    """
    Catch the log written by Python on console.
    """
    __log_dir = os.path.join(os.path.dirname(__file__), "..") + "/test_output/log_files/"
    __KEEP_LOG_FLAG = "-l"
    __LOG_LVL = logging.DEBUG

    __old_stdout = sys.stdout
    __stdout_fd = __old_stdout.fileno()
    __saved_stdout_fd = os.dup(__stdout_fd)

    __old_stderr = sys.stderr
    __stderr_fd = __old_stderr.fileno()
    __saved_stderr_fd = os.dup(__stderr_fd)

    def __init__(self, test_name: str):
        Logger.__init_log_folder()
        self.__log_file_path = "{}{}_{}.log".format(Logger.__log_dir, test_name,
                                                    str(time.strftime("%Y-%m-%d_%H-%M-%S")))

        self.__temp_file = tempfile.TemporaryFile(mode="w+t")
        Logger.__redirect_stdout_stderr(self.__temp_file)

    def save_log(self, test_status: str = Status.FAILED):
        """
        If "-l" is exist in sys.argv or test_status is Failed then keeping the log file.
        If test_status is Passed and missing "-l" from sys.argv then deleting log file.

        :param test_status: Passed of Failed.
        """
        Logger.__restore_stdout_stderr()

        self.__temp_file.seek(0)
        content = self.__temp_file.read()
        self.__temp_file.close()
        print(content)
        if test_status == Status.FAILED or Logger.__KEEP_LOG_FLAG in sys.argv:
            with open(self.__log_file_path, "w") as log:
                log.write(content)

        if os.path.isfile(self.__log_file_path):
            print(Colors.OKBLUE + "Log file has been kept at: {}\n".format(self.__log_file_path) + Colors.ENDC)

    @staticmethod
    def __redirect_stdout_stderr(file):
        """
        Redirect sys.stdout and sys.stderr to file.
        :param file: file that stdout and stderr is redirected to.
        """
        if not isinstance(file, io.IOBase):
            return
        os.dup2(file.fileno(), Logger.__stderr_fd)
        os.dup2(file.fileno(), Logger.__stdout_fd)

    @staticmethod
    def __restore_stdout_stderr():
        """
        Restore sys.stdout and sys.stderr to default.
        """
        os.dup2(Logger.__saved_stdout_fd, Logger.__stdout_fd)
        os.close(Logger.__saved_stdout_fd)
        sys.stdout = Logger.__old_stdout

        os.dup2(Logger.__saved_stderr_fd, Logger.__stderr_fd)
        os.close(Logger.__saved_stderr_fd)
        sys.stderr = Logger.__old_stderr

    @staticmethod
    def __init_log_folder():
        """
        Create log_files folder if it is not exist.

        :raise OSError.
        """
        try:
            os.makedirs(Logger.__log_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e
