"""
Created on Dec 8, 2017

@author: nhan.nguyen
"""

from indy import pool
from libraries.constant import Constant
from libraries.result import Status
from libraries.common import Common
from libraries import utils
from test_scripts.pool.pool_test_base import PoolTestBase


class TestOpenPoolLedgerConfig(PoolTestBase):

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        self.steps.add_step("Create pool ledger config")
        await utils.perform_and_raise_exception(self.steps, Common.create_pool_ledger_config,
                                                self.pool_name, Constant.pool_genesis_txn_file)
        # 2. Open pool ledger.
        self.steps.add_step("Open pool ledger")
        result = await utils.perform(self.steps, pool.open_pool_ledger, self.pool_name, None)

        # 3. Verify that returned pool_handle is a positive integer.
        self.steps.add_step("Verify that returned pool_handle is a positive integer")
        if not isinstance(result, Exception):
            self.pool_handle = result
            step = self.steps.get_last_step()
            if not isinstance(self.pool_handle, int) or self.pool_handle < 0:
                step.set_status(Status.FAILED)
                step.set_message("Cannot open pool ledger")
            else:
                step.set_status(Status.PASSED)


if __name__ == "__main__":
    TestOpenPoolLedgerConfig().execute_scenario()
