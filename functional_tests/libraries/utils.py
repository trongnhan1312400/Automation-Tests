"""
Created on Nov 9, 2017

@author: khoi.ngo

Containing all functions used by several test steps on test scenarios.
"""
from indy.error import IndyError
from .constant import Colors
from .result import Status


def generate_random_string(prefix="", suffix="", size=20):
    """
    Generate random string .

    :param prefix: (optional) Prefix of a string.
    :param suffix: (optional) Suffix of a string.
    :param size: (optional) Max length of a string (include prefix and suffix)
    :return: The random string.
    """
    import random
    import string
    left_size = size - len(prefix) - len(suffix)
    random_str = ""
    if left_size > 0:
        random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(left_size))
    else:
        print("Warning: Length of prefix and suffix more than %s chars" % str(size))
    result = str(prefix) + random_str + str(suffix)
    return result


def raise_if_exception(code):
    """
    If "code" is an exception then raise the "code".
    Unless "code" is an exception then return the "code".
    :param code: (optional) code that you want to check.
    :return: "code" if it is not an exception.
    """
    if isinstance(code, IndyError or Exception):
        raise code
    else:
        return code


async def perform(steps, func, *agrs):
    """
    Execute an function and set status, message for the last test step depend on the result of the function.

    :param steps: (optional) list of test steps.
    :param func: (optional) executed function.
    :param agrs: argument of function.
    :return: the result of function of the exception that the function raise.
    """
    try:
        result = await func(*agrs)
        steps.get_last_step().set_status(Status.PASSED)
    except IndyError as E:
        print(Colors.FAIL + "IndyError: " + str(E) + Colors.ENDC)
        steps.get_last_step().set_message(str(E))
        steps.get_last_step().set_status(Status.FAILED)
        return E
    except Exception as Ex:
        print(Colors.FAIL + "Exception: " + str(E) + Colors.ENDC)
        steps.get_last_step().set_message(str(Ex))
        steps.get_last_step().set_status(Status.FAILED)
        return Ex
    return result


async def perform_with_expected_code(steps, func, *agrs, expected_code=0):
    """
    Execute the "func" with expectation that the "func" raise an IndyError that IndyError.error_code = "expected_code".

    :param steps: (optional) list of test steps.
    :param func: (optional) executed function.
    :param agrs: arguments of "func".
    :param expected_code: the error code that you expect in IndyError.
    :return: exception if the "func" raise it without "expected_code".
             'None' if the "func" run without any exception of the exception contain "expected_code".
    """
    try:
        await func(*agrs)
        steps.get_last_step().set_message("Can execute without exception.")
        steps.get_last_step().set_status(Status.FAILED)
        return None
    except IndyError as E:
        if E.error_code == expected_code:
            steps.get_last_step().set_status(Status.PASSED)
            return None
        else:
            print(Colors.FAIL + "IndyError: " + str(E) + Colors.ENDC)
            steps.get_last_step().set_message(str(E))
            return E
    except Exception as Ex:
        print(Colors.FAIL + "Exception: " + str(E) + Colors.ENDC)
        return Ex


def run_async_method(method, time_out=None):
    """
    Run async method until it complete or until the time is over.

    :param method: (optional).
    :param time_out:
    """
    import asyncio
    loop = asyncio.new_event_loop()
    if not time_out:
        loop.run_until_complete(method())
    else:
        loop.run_until_complete(asyncio.wait_for(method(), time_out))
    loop.close()


def make_final_result(test_result, steps, begin_time, logger):
    """
    Making a test result.

    :param test_result: (optional).
    :param steps: (optional) list of steps.
    :param begin_time: (optional) time that the test begin.
    :param logger: (optional).
    """
    import time
    for step in steps:
        test_result.add_step(step)
        if step.get_status() == Status.FAILED:
            print('%s: ' % str(step.get_id()) + Colors.FAIL + 'failed\nMessage: ' + step.get_message() + Colors.ENDC)
            test_result.set_test_failed()

    test_result.set_duration(time.time() - begin_time)
    test_result.write_result_to_file()
    logger.save_log(test_result.get_test_status())
