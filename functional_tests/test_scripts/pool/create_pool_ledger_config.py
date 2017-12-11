"""
Created on Dec 8, 2017

@author: nhan.nguyen
"""

from libraries import utils
from libraries.constant import Constant
from libraries.result import Status
from libraries.common import Common
from test_scripts.pool.pool_test_base import PoolTestBase


class TestCreatePoolLedgerConfig(PoolTestBase):

    async def execute_test_steps(self):
        # 1. Create a pool ledger config.
        self.steps.add_step("Create pool ledger config")
        result = await utils.perform(self.steps, Common.create_pool_ledger_config,
                                     self.pool_name, Constant.pool_genesis_txn_file)

        # 2. Verify that pool ledger config is created.
        self.steps.add_step("Verify that pool ledger config is created")
        if not isinstance(result, Exception or IndexError):
            step = self.steps.get_last_step()
            if not utils.check_pool_exist(self.pool_name):
                message = "Cannot create a pool ledger config"
                step.set_message(message)
                step.set_status(Status.FAILED)
            else:
                step.set_status(Status.PASSED)


if __name__ == "__main__":
    TestCreatePoolLedgerConfig().execute_scenario()
