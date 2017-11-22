'''
Created on Nov 22, 2017

@author: tien.anh.nguyen
'''

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.utils import *
from libraries.constant import Constant
from libraries.common import Common


class TestScenarioBase(object):
    """
    Test base....
    """
    pool_name = generate_random_string("test_pool")
    wallet_name = generate_random_string("test_wallet")
    pool_genesis_txn_file = Constant.pool_genesis_txn_file
    logger = None
    steps = None
    test_result = None

    def init_test_data(self):
        pass

    def execute_precondition_steps(self):
        Common.clean_up_pool_and_wallet_folder(self.pool_name, self.wallet_name)

    def execute_test_case(self):
        pass

    def execute_scenario(self):
        self.init_test_data()
        self.execute_precondition_steps()
        self.execute_test_case()
        '''
        begin_time = time.time()
        self.steps.test_report.setup_json_report()

        #Precondition
        self.execute_precondition_steps()

        # Run test case and collect result
        Common.run(self.execute_test_case)
        #self.execute_test_case()
        Common.final_result(self.test_report, self.steps, begin_time)
        '''


if __name__ == '__main__':
    test_scenario = TestScenarioBase()
    test_scenario.execute_scenario()
