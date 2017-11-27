"""
Created on Nov 22, 2017

@author: khoi.ngo

Containing the test base class.
"""
import time
import sys
import os
import inspect
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.utils import *
from libraries.constant import Constant, Colors
from libraries.common import Common
from libraries.logger import Logger
from libraries.result import TestResult
from libraries.step import Steps


class TestScenarioBase(object):
    """
    Test base....
    All test scenario should inherit from this class.
    This class controls the work flow and hold some general test data for test scenarios that inherit it.
    """
    def __init__(self):
        """
        Init test data.
        If the test case need some extra test date then just override this method.
        """
        test_name = os.path.splitext(os.path.basename(inspect.getfile(self.__class__)))[0]
        self.test_result = TestResult(test_name)
        self.steps = Steps()
        self.logger = Logger(test_name)
        self.pool_name = generate_random_string("test_pool")
        self.wallet_name = generate_random_string("test_wallet")
        self.pool_handle = 0
        self.wallet_handle = 0
        self.pool_genesis_txn_file = Constant.pool_genesis_txn_file
        self.time_out = 300

    async def execute_precondition_steps(self):
        """
         Execute pre-condition of test scenario.
         If the test case need some extra step in pre-condition then just override this method.
        """
        Common.clean_up_pool_and_wallet_folder(self.pool_name, self.wallet_name)

    async def execute_postcondition_steps(self):
        """
        Execute post-condition of test scenario.
        If the test case need some extra step in post-condition then just override this method.
        """
        await Common.clean_up_pool_and_wallet(self.pool_name, self.pool_handle, self.wallet_name, self.wallet_handle)

    async def execute_test_steps(self):
        """
        The method where contain all main script of a test scenario.
        All test scenario inherit TestScenarioBase have to override this method.
        """
        pass

    def execute_scenario(self):
        """
        Execute the test scenario and control the work flow of this test scenario.
        """
        self.__init__()
        begin_time = time.time()

        try:
            run_async_method(self.execute_precondition_steps, self.time_out)
            run_async_method(self.execute_test_steps, self.time_out)
        except TimeoutError:
            print(Colors.FAIL + "\nTerminate test scenario because of time limit!!!\n" + Colors.ENDC)
        except Exception as e:
            print("\n\t{}\n".format(str(e)))
        finally:
            run_async_method(self.execute_postcondition_steps)
            make_final_result(self.test_result, self.steps.get_list_step(), begin_time, self.logger)
