"""
Created on Dec 8, 2017

@author: nhan.nguyen
"""

from indy import pool
from libraries.constant import Constant
from libraries.result import Status
from libraries import utils
from libraries.common import Common
from test_scripts.pool.pool_test_base import PoolTestBase


class TestCloseReopenedPoolLedgerConfig(PoolTestBase):

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await Common.create_and_open_pool_ledger_for_steps(self.steps, self.pool_name,
                                                                              Constant.pool_genesis_txn_file)

        # 3. Close pool ledger.
        self.steps.add_step("Close pool ledger")
        await utils.perform_and_raise_exception(self.steps, pool.close_pool_ledger, self.pool_handle)

        # 4. Reopen pool ledger.
        self.steps.add_step("Reopen pool ledger")
        self.pool_handle = await utils.perform_and_raise_exception(self.steps, pool.open_pool_ledger,
                                                                   self.pool_name, None)

        # 5. Close reopened pool ledger.
        self.steps.add_step("Close reopened pool ledger")
        result = await utils.perform(self.steps, pool.close_pool_ledger, self.pool_handle)

        # 6. Verify that reopened pool ledger is closed successfully.
        self.steps.add_step("Verify that reopened pool ledger is closed successfully")
        step = self.steps.get_last_step()
        if result is not None:
            step.set_status(Status.FAILED)
            step.set_message("Cannot close reopened pool ledger")
        else:
            step.set_status(Status.PASSED)
            self.pool_handle = None  # prevent post-condition close pool ledger again.


if __name__ == "__main__":
    TestCloseReopenedPoolLedgerConfig().execute_scenario()
