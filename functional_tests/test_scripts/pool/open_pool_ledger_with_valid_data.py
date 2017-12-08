"""
Created on Dec 8, 2017

@author: nhan.nguyen
"""

from libraries.constant import Constant
from libraries.result import Status
from libraries.common import Common
from test_scripts.pool.pool_test_base import PoolTestBase


class TestOpenPoolLedgerConfig(PoolTestBase):

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        result = await Common.create_and_open_pool_ledger_for_steps(self.steps, self.pool_name,
                                                                    Constant.pool_genesis_txn_file)

        # 3. Verify that returned pool_handle is a positive integer.
        self.steps.add_step("Verify that returned pool_handle is a positive integer")
        if not isinstance(result, Exception):
            self.pool_handle = result
            if isinstance(result, int) and self.pool_handle < 0:
                step = self.steps.get_last_step()
                step.set_status(Status.FAILED)
                step.set_message("Cannot open pool ledger")


if __name__ == "__main__":
    TestOpenPoolLedgerConfig().execute_scenario()
