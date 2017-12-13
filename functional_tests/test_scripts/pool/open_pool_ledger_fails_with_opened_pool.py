"""
Created on Dec 12, 2017

@author: nhan.nguyen
"""

from indy import pool
from indy.error import ErrorCode
from libraries.constant import Constant
from libraries.common import Common
from libraries import utils
from test_scripts.pool.pool_test_base import PoolTestBase


class TestOpenAOpenedPoolLedger(PoolTestBase):
    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        self.steps.add_step("Create pool ledger config")
        await utils.perform(self.steps, Common.create_pool_ledger_config,
                            self.pool_name, Constant.pool_genesis_txn_file)
        # 2. Open pool ledger.
        self.steps.add_step("Open pool ledger")
        self.pool_handle = await utils.perform(self.steps,
                                               pool.open_pool_ledger,
                                               self.pool_name, None)

        # 3. Reopen a opened pool ledger
        # and verify that cannot reopen a opened pool ledger.
        self.steps.add_step("Reopen a opened pool ledger and "
                            "verify that cannot reopen a opened pool ledger")
        error_code = ErrorCode.PoolLedgerInvalidPoolHandle
        await utils.perform_with_expected_code(self.steps,
                                               pool.open_pool_ledger,
                                               self.pool_name, None,
                                               expected_code=error_code)


if __name__ == "__main__":
    TestOpenAOpenedPoolLedger().execute_scenario()
