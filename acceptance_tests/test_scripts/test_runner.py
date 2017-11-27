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
from threading import Timer
from indy import IndyError


class TestRunner:
    __SEPARATOR = "="
    __EXECUTOR = "python3.6"
    __default_dir = os.path.dirname(os.path.abspath(__file__))
    __reporter_dir = __default_dir + "/reporter.py"

    def __init__(self):
        self.__argv_for_test_runner = {"-d": None, "-t": None, "-html": None}
        self.__test_process = None
        self.__current_scenario = None
        self.__continue = True
        self.__catch_arg()
        pass

    def run(self):
        """
        Run all test scenario and then execute reporter if -html flag exist.
        """
        list_test_files = []
        temp = self.__argv_for_test_runner["-d"]
        test_directiory = temp if temp is not None else TestRunner.__default_dir

        if not os.path.exists(test_directiory) or not os.path.isdir(test_directiory):
            print("Directory is incorrect!")
            return

        list_test_files = TestRunner.__get_list_files(test_directiory)

        if not list_test_files:
            print("Cannot find any test cases!")
            return

        for test_scenario_file in list_test_files:
            if self.__continue:
                self.__execute_test_scenario(test_scenario_file)

        self.__execute_reporter()

    def run_with_time_out(self):
        """
        Execute the "self.run" function with timeout.
        Timeout is from sys.argv.
        """
        time_out = self.__argv_for_test_runner["-t"]
        try:
            if time_out:
                time_out = float(time_out)
        except ValueError:
            print("Time out is not a number")
            return

        if not time_out:
            self.run()
            print("\033[92m" + "\nAll tests have been executed!!!\n" + "\033[0m")
        else:
            timer = Timer(float(time_out), function=self.__timeout_event)
            timer.start()
            self.run()
            if timer.is_alive():
                timer.cancel()
            if self.__continue:
                print("\033[92m" + "\nAll tests have been executed!!!\n" + "\033[0m")
            else:
                self.__continue = False

    def __timeout_event(self):
        """
        Terminate current test scenario and run it's pos-condition.
        :return:
        """
        self.__continue = False
        print("\033[91m" + "\nAborting test scenario because of time limitation...\n" + "\033[0m")
        print("\033[95m" + "Running clean up for aborted test scenario..." + "\033[0m")
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
        args = self.__argv_for_test_runner
        for arg in args:
            if arg in sys.argv:
                index = sys.argv.index(arg)
                if index < len(sys.argv) - 1:
                    temp = sys.argv[index + 1]
                    self.__argv_for_test_runner[arg] = temp if temp not in args else ""

    def __execute_reporter(self):
        """
        Execute html_reporter if -html flag is exist in sys.argv.
        """
        report_path = self.__argv_for_test_runner["-html"]
        if report_path is "":
            return
        report_path = report_path if report_path else TestRunner.__reporter_dir
        cmd = "{} {}".format(TestRunner.__EXECUTOR, report_path)
        subprocess.call(cmd, shell=True)

    def __execute_test_scenario(self, test_scenario_file: str):
        """
        Find all scenario in "test_scenario_file" and execute them.
        :param test_scenario_file: file that contain test scenarios.
        """
        if not test_scenario_file:
            return
        sys.path.append(os.path.dirname(os.path.abspath(test_scenario_file)))
        test_module = importlib.import_module(os.path.basename(test_scenario_file).replace(".py", ""))
        for name, cls in inspect.getmembers(test_module, inspect.isclass):
            if "TestScenarioBase" in str(cls.__bases__):
                test_scenario = cls()
                process = multiprocessing.Process(target=test_scenario.execute_scenario)
                self.__current_scenario = test_scenario
                self.__test_process = process
                process.start()
                process.join()

    @staticmethod
    def __get_list_files(star_directory):
        """
        Get all .py file in star directory and sub directories.
        :param star_directory:
        """
        list_files = []
        try:
            for directory, _, _ in os.walk(star_directory):
                list_files.extend(glob.glob(os.path.join(directory, "*.py")))
        except Exception as e:
            print(str(e))

        return list_files


if __name__ == "__main__":
    TestRunner().run_with_time_out()
