import errno
import os
import sys
import time

import pytest

import reporter
from utilities import result, utils


def pytest_runtest_logreport(report):
    """
    Catch and save the log if test failed of option keep log (-l) exist.

    :param report: report of pytest that contains log.
    """
    if report.failed or '-l' in sys.argv:
        def init_folder(folder):
            try:
                os.makedirs(folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise e

        log_dir = utils.get_project_path() + "/test_output/log_files/"

        init_folder(log_dir)

        # Get test's name.
        cur_time = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
        path_to_test = report.nodeid.split("::")[0]
        test_name = "{}_{}.log".format(os.path.basename(path_to_test),
                                       cur_time)

        log_path = log_dir + test_name

        log = ""
        for header, content in report.sections:
            log += "\n" + (' {0} '.format(header).center(80, '-'))
            log += "\n" + content

        with open(log_path, "w") as log_file:
            log_file.write(log)


@pytest.fixture(scope="session", autouse=True)
def make_json_summary(request):
    """
    Make json summary report after session if there is a option to generate
    html report.

    :param request:
    """
    yield
    if request.config.getoption("htmlpath") is not None:
        with open("abc.txt", "w") as f:
            f.write(str(result.Result.result_of_all_tests))
        reporter.JsonSummaryReport().generate_report_from_file(
            result.Result.result_of_all_tests)
