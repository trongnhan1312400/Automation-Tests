'''
Created on Nov 9, 2017

@author: khoi.ngo
'''


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


def create_step(size):
    from libraries.step import Step
    lst_step = []
    for i in range(0, size):
        step = Step(i, "")
        lst_step.append(step)
    return lst_step


def raise_if_exception(code):
    """
    If "code" is an exception then raise the "code".
    Unless "code" is an exception then return the "code".
    :param code: (optional) code that you want to check.
    :return: "code" if it is not an exception
    """
    if isinstance(code, IndexError or Exception):
        raise code
    else:
        return code


async def perform(step, func, *agrs):
    """
    Execute an function and set status, message for the test step
    depend on the result of the function.
    :param step: (optional) test step involve with "func".
    :param func: (optional) executed function.
    :param agrs: argument of function.
    :return: the result of function of the exception that the function raise.
    """
    from indy.error import IndyError
    from libraries.result import Status
    try:
        result = await func(*agrs)
        step.set_status(Status.PASSED)
    except IndyError as E:
        print("Indy error" + str(E))
        step.set_message(str(E))
        step.set_status(Status.FAILED)
        return E
    except Exception as Ex:
        print("Exception" + str(Ex))
        step.set_message(str(Ex))
        step.set_status(Status.FAILED)
        return Ex
    return result


async def perform_with_expected_code(step, func, *agrs, expected_code=0):
    """
    Execute the "func" with expectation that the "func" raise an IndyError
    that IndyError.error_code = "expected_code".
    :param step: (optional) test step involve with the "func".
    :param func: (optional) executed function.
    :param agrs: arguments of "func".
    :param expected_code: the error code that you expect in IndyError.
    :return: exception if the "func" raise it without "expected_code"
             'None' if the "func" run without any exception of the exception contain "expected_code"
    """
    from indy.error import IndyError
    from libraries.result import Status
    try:
        await func(*agrs)
        step.set_message("Can execute without exception.")
        step.set_status(Status.FAILED)
        return None
    except IndyError as E:
        if E.error_code == expected_code:
            step.set_status(Status.PASSED)
            return None
        else:
            print("Indy error" + str(E))
            step.set_message(str(E))
            return E
    except Exception as Ex:
        print("Exception" + str(Ex))
        return Ex
