import os
import sys
import errno
import time


def pytest_runtest_logreport(report):
    if report.failed or '-l' in sys.argv:
        def init_folder(folder):
            try:
                os.makedirs(folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise e

        log_dir = os.path.join(os.path.dirname(
            __file__), "..") + "/test_output/log_files/"

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
