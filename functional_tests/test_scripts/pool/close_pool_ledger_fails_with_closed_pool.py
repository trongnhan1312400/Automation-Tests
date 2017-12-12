"""
Created on Dec 12, 2017

@author: nhan.nguyen
"""

from indy import pool
from indy.error import ErrorCode
from libraries.constant import Constant
from libraries import utils
from libraries.common import Common
from test_scripts.pool.pool_test_base import PoolTestBase


class TestCloseAClosedPoolLedger(PoolTestBase):

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await Common.create_and_open_pool_ledger_for_steps(self.steps, self.pool_name,
                                                                              Constant.pool_genesis_txn_file)

        # 3. Close pool ledger.
        self.steps.add_step("Close pool ledger")
        await utils.perform(self.steps, pool.close_pool_ledger, self.pool_handle)

        # 4. Close a closed pool ledger verify that closed pool ledger cannot be closed.
        self.steps.add_step("Close a closed pool ledger verify that closed pool ledger cannot be closed")
        await utils.perform_with_expected_code(self.steps, pool.close_pool_ledger, self.pool_handle,
                                               expected_code=ErrorCode.PoolLedgerInvalidPoolHandle)
        self.pool_handle = None  # prevent post-condition close pool again.


if __name__ == "__main__":
    TestCloseAClosedPoolLedger().execute_scenario()
