"""
Created on Nov 24, 2017

@author: nhan.nguyen

Containing class for Test Runner.
"""

import subprocess
import os
import glob
import sys
import asyncio
import inspect
import importlib
import multiprocessing
import argparse
from threading import Timer
from indy import IndyError
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from libraries.constant import Colors, Message


class TestRunner:
    __default_dir = os.path.dirname(os.path.abspath(__file__))
    __reporter_dir = __default_dir + "/reporter.py"

    def __init__(self):
        self.__args_for_test_runner = None
        self.__test_process = None
        self.__current_scenario = None
        self.__continue = True
        self.__catch_arg()
        pass

    def run(self):
        """
        Run all test scenario and then execute reporter if -html flag exist.
        """
        temp = self.__args_for_test_runner.directory
        test_directiory = temp if temp else TestRunner.__default_dir

        if not os.path.exists(test_directiory) or not os.path.isdir(test_directiory):
            print(Message.ERR_PATH_DOES_NOT_EXIST)
            return

        list_test_scenarios = TestRunner.__get_list_scenarios_in_folder(test_directiory)

        if not list_test_scenarios:
            print(Message.ERR_CANNOT_FIND_ANY_TEST_SCENARIOS)
            return

        for test_scenario in list_test_scenarios:
            if self.__continue:
                self.__execute_test_scenario(test_scenario)

        self.__execute_reporter()

    def run_with_time_out(self):
        """
        Execute the "self.run" function with timeout.
        Timeout is from sys.argv.
        """
        time_out = self.__args_for_test_runner.timeout

        if not time_out or time_out <= 0:
            self.run()
            print(Colors.OKGREEN + "\n{}\n".format(Message.INFO_ALL_TEST_HAVE_BEEN_EXECUTED) + Colors.ENDC)
        else:
            timer = Timer(float(time_out), function=self.__timeout_event)
            timer.start()
            self.run()
            if timer.is_alive():
                timer.cancel()
            if self.__continue:
                print(Colors.OKGREEN + "\n{}\n".format(Message.INFO_ALL_TEST_HAVE_BEEN_EXECUTED) + Colors.ENDC)
            else:
                self.__continue = False

    def __timeout_event(self):
        """
        Terminate current test scenario and run it's pos-condition.
        """
        self.__continue = False
        print(Colors.FAIL + "\n{}\n".format(Message.ERR_TEST_RUNNER_TIME_LIMITATION) + Colors.ENDC)
        print(Colors.HEADER + "{}".format(Message.INFO_RUNNING_TEST_POS_CONDITION) + Colors.ENDC)
        if self.__test_process:
            self.__test_process.terminate()
        if self.__current_scenario:
            try:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.__current_scenario.execute_postcondition_steps())
                loop.close()
            except IndyError:
                pass

    def __catch_arg(self):
        """
        Catch args for TestRunner in sys.argv.
        """
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-d", "--directory", dest="directory", help="directory of test scenarios",
                                default="", nargs="?")
        arg_parser.add_argument("-t", "--timeout", dest="timeout", type=float, help="time out of test runner",
                                default=-1.0, nargs="?")
        arg_parser.add_argument("-html", "--html_reporter", dest="reporter",
                                help="path to html reporter. If this arg is "
                                     "missing, html report would not be generated",
                                default="", nargs="?")
        arg_parser.add_argument("-l", "--keep_log", action='store_true',  help="keep all log file")
        self.__args_for_test_runner = arg_parser.parse_args()

    def __execute_reporter(self):
        """
        Execute html_reporter if -html flag is exist in sys.argv.
        """
        reporter_path = self.__args_for_test_runner.reporter
        if reporter_path is "":
            return
        reporter_path = reporter_path if reporter_path else TestRunner.__reporter_dir
        cmd = "{} {}".format("python3.6", reporter_path)
        subprocess.call(cmd, shell=True)

    def __execute_test_scenario(self, test_scenario):
        """
        Execute test scenario.
        :param test_scenario: file that contain test scenarios.
        """
        if not test_scenario:
            return
        self.__current_scenario = test_scenario()
        process = multiprocessing.Process(target=self.__current_scenario.execute_scenario)
        self.__test_process = process
        process.start()
        process.join()

    @staticmethod
    def __get_list_scenarios_in_folder(start_directory):
        """
        Get all test scenarios in start directory and sub directories.
        :param start_directory:
        """
        list_files = []

        try:
            for directory, _, _ in os.walk(start_directory):
                list_files.extend(glob.glob(os.path.join(directory, "*.py")))
        except Exception:
            pass

        list_test_scenarios = []
        for file in list_files:
            sys.path.append(os.path.dirname(os.path.abspath(file)))
            test_module = importlib.import_module(os.path.basename(file).replace(".py", ""))
            for name, cls in inspect.getmembers(test_module, inspect.isclass):
                if "TestScenarioBase" in str(cls.__bases__):
                    list_test_scenarios.append(cls)

        return list_test_scenarios


if __name__ == "__main__":
    TestRunner().run_with_time_out()
