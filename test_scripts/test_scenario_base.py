"""
Created on Nov 22, 2017

@author: khoi.ngo


"""
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.utils import *
from libraries.constant import Constant
from libraries.common import Common
from libraries.logger import Logger
from libraries.result import TestResult
from libraries.step import Steps


class TestScenarioBase(object):
    """
    Test base....
    All test scenario should inherit from this class.
    This class control the work flow and hold some general test data for test scenario that inherit it.
    """
    pool_name = generate_random_string("test_pool")
    wallet_name = generate_random_string("test_wallet")
    pool_handle = 0
    wallet_handle = 0
    pool_genesis_txn_file = Constant.pool_genesis_txn_file
    logger = None
    steps = None
    test_result = None

    def __init__(self, test_name):
        """
        Init some specify data that is different among sub test classes.
        Should be called first by super().__init__ in all sub test classes.
        :param test_name: name of test case.
        """
        self.test_result = TestResult(test_name)
        self.steps = Steps()
        self.logger = Logger(test_name)

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
        begin_time = time.time()
        Common.run_async_method(self.execute_precondition_steps)
        Common.run_async_method(self.execute_test_case)
        Common.run_async_method(self.execute_postcondition_steps)
        Common.make_final_result(self.test_result, self.steps.get_list_step(), begin_time, self.logger)

