"""
Created on Nov 12, 2017

@author: nghia.huynh

Containing all functions and classes to make a HTML report.
"""
import os
import json
import socket
import platform
import glob
import subprocess
import errno
import argparse
import time


def get_version(program: str) -> str:
    """
    Return version of a program.

    :param program: program's name.
    :return: version.
    """
    cmd = "dpkg -l | grep '{}'".format(program)
    process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    (out, _) = process.communicate()
    result = out.decode()
    version = result.split()

    if len(version) >= 3:
        if version[1] == program:
            return version[2]
    return "Cannot find version for '{}'".format(program)


class JsonSummaryReport:
    __default_dir = os.path.dirname(os.path.abspath(__file__))

    __json_dir = __default_dir + "/test_output/test_results/"

    __report_dir = __default_dir + "/reporter_summary_report/"

    __dependencies = ["indy-plenum", "indy-node", "indy-anoncreds", "sovrin"]

    __SYSTEM = "system_info"
    __OS = "os"
    __HOST_NAME = "host_name"
    __RESULTS = "test_results"
    __SUMMARY = "summary"
    __TOTAL_TESTS = "total_tests"
    __PASSED_TESTS = "passed_tests"
    __FAILED_TESTS = "failed_tests"
    __DURATION = "duration"

    def __init__(self):
        JsonSummaryReport.__init_report_folder()
        self.__json_content = dict()

    def generate_report_from_file(self, json_files: list):
        """
        Generate report from an list of json files.

        :param json_files:
        """
        print("Generating a html report...")
        report_file_name = JsonSummaryReport.__make_report_name()

        # Write to file.
        summary_json_file = self.__report_dir + report_file_name + ".json"
        self.__make_system_info()
        self.__make_result(json_files)

        # With json summary to file.
        with open(summary_json_file, "w+") as json_summary:
            json.dump(self.__json_content, json_summary,
                      ensure_ascii=False, indent=2, sort_keys=True)

    def generate_report_from_filter(self, file_filter):
        """
        Generate report form filter.

        :param file_filter:
        :return:
        """
        file_filter = "*" if not file_filter else file_filter
        list_file_name = glob.glob(self.__json_dir + file_filter + ".json")
        if not list_file_name:
            print("Cannot find any json at {}".format(
                JsonSummaryReport.__json_dir))
            return

        self.generate_report_from_file(list_file_name)

    def __make_system_info(self):
        system_info = dict()
        system_info[JsonSummaryReport.__HOST_NAME] = socket.gethostname()
        system_info[JsonSummaryReport.__OS] = (platform.system() +
                                               platform.release())

        for dependency in JsonSummaryReport.__dependencies:
            system_info[dependency] = get_version(dependency)

        self.__json_content[JsonSummaryReport.__SYSTEM] = system_info

    def __make_result(self, list_files):
        test_results = list()
        test_passed = test_failed = 0
        total = len(list_files)
        duration = 0
        for file in list_files:
            test_result = json.load(open(file))
            if test_result["result"].lower() == "passed":
                test_passed += 1
            else:
                test_failed += 1
            duration += test_result["duration"]
            test_results.append(test_result)

        # Make summary.
        summary = dict()
        summary[JsonSummaryReport.__TOTAL_TESTS] = total
        summary[JsonSummaryReport.__PASSED_TESTS] = test_passed
        summary[JsonSummaryReport.__FAILED_TESTS] = test_failed
        summary[JsonSummaryReport.__DURATION] = duration

        self.__json_content[JsonSummaryReport.__SUMMARY] = summary
        self.__json_content[JsonSummaryReport.__RESULTS] = test_results

    @staticmethod
    def __make_report_name() -> str:
        """
        Generate report name.
        :return: report name.
        """
        name = "Summary_{}".format(str(time.strftime("%Y-%m-%d_%H-%M-%S")))

        return name

    @staticmethod
    def __init_report_folder():
        """
        Create reporter_summary_report directory if it not exist.
        :raise OSError.
        """
        try:
            os.makedirs(JsonSummaryReport.__report_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e


if __name__ == "__main__":
    reporter = JsonSummaryReport()
    # Get argument from sys.argv to make filters
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-n", "--name", dest="name", nargs="?",
                            default=None, help="filter json file by name")
    args = arg_parser.parse_args()
    json_filter = args.name

    # Generate a html report
    reporter.generate_report_from_filter(json_filter)
