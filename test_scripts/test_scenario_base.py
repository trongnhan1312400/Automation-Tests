'''
Created on Nov 22, 2017

@author: tien.anh.nguyen
'''
import time
import sys
import os
from indy.error import IndyError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.utils import *
from libraries.constant import Constant
from libraries.common import Common
from libraries.logger import Logger
from libraries.result import TestResult


class TestScenarioBase(object):
    """
    Test base....
    """
    pool_name = generate_random_string("test_pool")
    wallet_name = generate_random_string("test_wallet")
    pool_handle = 0
    wallet_handle = 0
    pool_genesis_txn_file = Constant.pool_genesis_txn_file
    logger = None
    steps = None
    test_result = None

    def __init__(self, total_steps, test_name):
        self.test_result = TestResult(test_name)
        self.steps = create_step(total_steps)
        self.logger = Logger(test_name)

    def execute_precondition_steps(self):
        Common.clean_up_pool_and_wallet_folder(self.pool_name, self.wallet_name)

    async def execute_postcondition_steps(self):
        await Common.clean_up_pool_and_wallet(self.pool_name, self.pool_handle, self.wallet_name, self.wallet_handle)

    async def execute_test_case(self):
        pass

    def execute_scenario(self):
        begin_time = time.time()
        self.execute_precondition_steps()
        Common.run_async_method(self.execute_test_case)
        Common.run_async_method(self.execute_postcondition_steps)
        Common.make_final_result(self.test_result, self.steps, begin_time, self.logger)


if __name__ == '__main__':
    test_scenario = TestScenarioBase(0, "test_base")
    test_scenario.execute_scenario()
