"""
Created on Nov 9, 2017

@author: nhan.nguyen
"""

import json
import time
import os


class KeyWord:
    TEST_CASE = "testcase"
    RESULT = "result"
    START_TIME = "starttime"
    DURATION = "duration"
    RUN = "run"
    STEP = "step"
    STATUS = "status"
    MESSAGE = "message"


class Status:
    PASSED = "Passed"
    FAILED = "Failed"


class Printer(object):
    """
    Class that write content to several file.
    Use this class when you want to write log
    not only on console but only on some other files.
    """
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        """
        Write a content into several files.

        :param obj: content you want to write.
        """
        for f in self.files:
            f.write(obj)
            f.flush()  # Want this content is displayed immediately on file

    def flush(self):
        for f in self.files:
            f.flush()


class TestResult:
    __json_dir = os.path.join(os.path.dirname(__file__), "..") + "/test_output/test_results/"

    def __init__(self, test_case_name):
        """
        Constructor of a TestResult instance.

        :param test_case_name:
        """
        self.__test_result = {}  # Store information of a test case
        self.__run = []  # Store information of steps in test case
        self.__test_result[KeyWord.TEST_CASE] = test_case_name
        self.__test_result[KeyWord.RESULT] = Status.PASSED
        self.__test_result[KeyWord.START_TIME] = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
        self.__json_file_path = "{0}/{1}_{2}.json".format(TestResult.__json_dir, self.__test_result[KeyWord.TEST_CASE],
                                                          self.__test_result[KeyWord.START_TIME])

    def set_result(self, result):
        """
        Set a result (PASSED or FAILED) for test case.

        :param result:
        """
        self.__test_result[KeyWord.RESULT] = result

    def set_duration(self, duration):
        """
        Set duration for test.

        :param duration: (second)
        """
        self.__test_result[KeyWord.DURATION] = round(duration * 1000)

    def set_step_status(self, step_summary: str, status: str = Status.PASSED, message: str = None):
        """
        Set status and message for specify step.

        :param step_summary: title of step.
        :param status: PASSED or FAILED.
        :param message: anything that involve to step like Exception, Log,...
        """
        temp = {KeyWord.STEP: step_summary, KeyWord.STATUS: status, KeyWord.MESSAGE: message}
        self.__run.append(temp)

    def add_step(self, step):
        """
        Add a step to report
        :param step:
        :return:
        """
        if not step:
            return
        temp = {KeyWord.STEP: step.get_name(), KeyWord.STATUS: step.get_status(), KeyWord.MESSAGE: step.get_message()}
        self.__run.append(temp)

    def write_result_to_file(self):
        """
        Write the result as json.
        """
        self.__test_result[KeyWord.RUN] = self.__run
        with open(self.__json_file_path, "w+") as outfile:
            json.dump(self.__test_result, outfile, ensure_ascii=False, indent=2)

    def set_test_failed(self):
        """
        Set status of test to FAILED.
        """
        self.set_result(Status.FAILED)

    def set_test_passed(self):
        """
        Set status of test to PASSED.
        """
        self.set_result(Status.PASSED)

    def get_test_status(self) -> str:
        """
        Get the status of test
        :return: test status
        """
        return self.__test_result[KeyWord.RESULT]

    @staticmethod
    def __init_output_folder():
        """
        Create test_output directory if it not exist
        :return:
        """
        if not os.path.exists(TestResult.__json_dir):
            os.makedirs(TestResult.__json_dir)
