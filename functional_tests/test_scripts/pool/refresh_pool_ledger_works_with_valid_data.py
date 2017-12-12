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


class TestRefreshPoolLedgerConfig(PoolTestBase):

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await Common.create_and_open_pool_ledger_for_steps(self.steps, self.pool_name,
                                                                              Constant.pool_genesis_txn_file)

        # 3. Refresh pool ledger.
        self.steps.add_step("Refresh pool ledger")
        result = await utils.perform(self.steps, pool.refresh_pool_ledger, self.pool_handle)

        # 4. Verify that opened pool ledger can be refreshed.
        self.steps.add_step("Verify that opened pool ledger can be refreshed")
        utils.check(self.steps, error_message="Cannot refresh pool ledger",
                    condition=lambda:result is None)


if __name__ == "__main__":
    TestRefreshPoolLedgerConfig().execute_scenario()