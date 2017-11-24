"""
Created on Nov 24, 2017

@author: nhan.nguyen
"""

import subprocess
import os
import glob
import sys
import asyncio


class TestRunner:
    __NOT_RUN_FILES = ["reporter.py", "test_runner.py", "test_scenario_base.py", "__init__.py"]
    __SEPARATOR = "="
    __EXECUTOR = "python3.6"
    __default_dir = os.path.dirname(os.path.abspath(__file__))
    __reporter_dir = __default_dir + "/reporter.py"
    __argv_for_test_scenario = ["-l"]
    __flag_for_test_scenario = ["-l"]
    __argv_for_test_runner = {"-d": None, "-t": None, "-l": None, "-html": None}

    def __init__(self):
        self.__catch_arg()
        pass

    async def run(self):
        list_tests = []
        if self.__argv_for_test_runner["-d"] is not None:
            if self.__argv_for_test_runner["-d"] is "":
                print("Missing directory")
                exit(1)
            else:
                list_tests = TestRunner.__get_list_files(self.__argv_for_test_runner["-d"])
                print(self.__argv_for_test_runner["-d"])
        else:
            list_tests = TestRunner.__get_list_files(TestRunner.__default_dir)

        if not list_tests:
            print("Cannot find any test cases")
            exit(1)

        for test in list_tests:
            self.__execute_test_by_command(test)
        self.__execute_reporter()

    def run_with_time_out(self):
        """
        Execute the "self.run" function with timeout.
        Timeout is from sys.argv.
        """
        time_out = self.__argv_for_test_runner["-t"]
        loop = asyncio.new_event_loop()
        if not time_out:
            loop.run_until_complete(self.run())
        else:
            print(time_out)
            loop.run_until_complete(asyncio.wait_for(self.run(), float(time_out)))
        loop.close()

    def __catch_arg(self):
        for arg in sys.argv:
            temp = str(arg).split(TestRunner.__SEPARATOR)
            if temp[0] in TestRunner.__argv_for_test_runner:
                self.__argv_for_test_runner[temp[0]] = temp[1] if len(temp) == 2 else ""

    def __build_execute_test_command(self, test_path: str) -> str:
        cmd = "{} {}".format(TestRunner.__EXECUTOR, test_path)
        for arg in self.__argv_for_test_scenario:
            if arg in self.__argv_for_test_runner and self.__argv_for_test_runner[arg] is not None:
                if arg in self.__flag_for_test_scenario:
                    cmd = "{} {}".format(cmd, arg)
                else:
                    cmd = "{} {}={}".format(cmd, arg, self.__argv_for_test_runner[arg])
        return cmd

    def __execute_reporter(self):
        report_path = self.__argv_for_test_runner["-html"]
        if report_path is not None:
            if report_path is "":
                report_path = self.__reporter_dir
            cmd = "{} {}".format(TestRunner.__EXECUTOR, report_path)
            self.__execute_command(cmd)

    def __execute_test_by_command(self, test_path: str):
        cmd = self.__build_execute_test_command(test_path)
        print(cmd)
        TestRunner.__execute_command(cmd)

    @staticmethod
    def __get_list_files(star_directory):
        list_files = []
        try:
            list_files.extend(glob.glob(os.path.join(star_directory, "*.py")))
            for directory, _, _ in os.walk(star_directory):
                list_files.extend(glob.glob(os.path.join(directory, "*.py")))
            list_files = [f for f in list_files if os.path.basename(f) not in TestRunner.__NOT_RUN_FILES]
        except Exception as e:
            print(str(e))

        return list_files

    @staticmethod
    def __execute_command(cmd):
        subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    try:
        TestRunner().run_with_time_out()
    except TimeoutError:
        print("\n\nTerminate the TestRunner because time out!!!!!\n\n")
