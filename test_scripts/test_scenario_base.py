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
from libraries.constant import Colors, Constant
from libraries.common import Common
from libraries.logger import Logger
from libraries.result import TestResult, Status


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

    def init_test_data(self, total_steps, test_name):
        test_result = TestResult(test_name)
        steps = create_step(total_steps)
        logger = Logger(test_name)

    def execute_precondition_steps(self):
        Common.clean_up_pool_and_wallet_folder(self.pool_name, self.wallet_name)

    def execute_postcondition_steps(self):
        Common.clean_up_pool_and_wallet(self.pool_name, self.pool_handle, self.wallet_name, self.wallet_handle)

    def execute_test_case(self):
        pass

    def execute_scenario(self):
        begin_time = time.time()
        self.init_test_data()
        self.execute_precondition_steps()
        self.execute_test_case()
        self.execute_postcondition_steps()
        Common.final_result(self.test_report, self.steps, begin_time, self.logger)

if __name__ == '__main__':
    test_scenario = TestScenarioBase()
    test_scenario.execute_scenario()
