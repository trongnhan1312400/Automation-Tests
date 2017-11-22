import json
import os.path
import sys
from indy import pool
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.constant import Constant, Colors, Roles
from libraries.result import Status
from libraries.common import Common
from libraries.utils import *
from test_scripts.test_scenario_base import TestScenarioBase

""" Global variables. """
pool_genesis_txn_file = Constant.pool_genesis_txn_file
original_pool_genesis_txn_file = Constant.original_pool_genesis_txn_file
the_error_message = "the information needed to connect was not found"

""" cmds """
back_up_pool_genesis_file = 'cp ' + pool_genesis_txn_file + " " + original_pool_genesis_txn_file
exit_sovrin = 'exit'
remove_pool_genesis_file = 'rm ' + pool_genesis_txn_file
restore_pool_genesis_file = 'cp ' + original_pool_genesis_txn_file + " " + pool_genesis_txn_file


class TestScenario02(TestScenarioBase):

    def __init__(self):
        super().__init__(total_steps=3, test_name="test_scenario_02_verify_messages_on_connection")

    def run(self, cmd):
        os.system(cmd)

    def execute_precondition_steps(self):
        self.run(back_up_pool_genesis_file)
        open(pool_genesis_txn_file, 'w').close()

    async def execute_postcondition_steps(self):
        self.run(remove_pool_genesis_file)
        self.run(restore_pool_genesis_file)

    async def execute_test_case(self):
        print("Test Scenario 02 -> started")
        try:
            # 1. Create ledger config from genesis txn file  ---------------------------------------------------------
            step1 = self.steps[0]
            step1.set_name("Create Ledger")
            pool_config = json.dumps({"genesis_txn": str(self.pool_genesis_txn_file)})
            self.pool_handle = await perform(step1, pool.create_pool_ledger_config, self.pool_name, pool_config)

            # 2. Open pool ledger -----------------------------------------------------------------------------------
            step = 1
            self.steps[step].set_name("Open pool ledger")
            self.steps[step].set_message("Failed due to the Bug IS-332")
            self.steps[step].set_status(Status.FAILED)

            # 3. verifying the message ------------------------------------------------------------------------
            step = 2
            self.steps[step].set_name("verifying the message")
            self.steps[step].set_message("TODO after fix IS-332")
            self.steps[step].set_status(Status.FAILED)
        except Exception as ex:
            print(Colors.FAIL + "Exception: " + str(ex) + Colors.ENDC)

        print("Test Scenario 02 -> completed")


if __name__ == '__main__':
    TestScenario02().execute_scenario()
