"""
Created on Dec 8, 2017

@author: nhan.nguyen
"""

from indy import pool
from libraries import utils
from libraries.constant import Constant
from libraries.result import Status
from libraries.common import Common
from test_scripts.pool.pool_test_base import PoolTestBase


class TestDeletePoolLedgerConfig(PoolTestBase):

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        self.steps.add_step("Create pool ledger config")
        await utils.perform(self.steps, Common.create_pool_ledger_config,
                            self.pool_name, Constant.pool_genesis_txn_file)

        # 2. Delete created pool ledger config.
        self.steps.add_step("Delete created pool ledger config")
        result = await utils.perform(self.steps, pool.delete_pool_ledger_config, self.pool_name)

        # 3. Verify that pool ledger config is deleted.
        self.steps.add_step("Verify that pool ledger config is deleted")
        if utils.check(self.steps, error_message="Cannot delete a pool ledger config",
                       condition=lambda: not isinstance(result, Exception) and
                       not utils.check_pool_exist(self.pool_name)):
                self.pool_name = None   # prevent post-condition clean up the pool again.


if __name__ == "__main__":
    TestDeletePoolLedgerConfig().execute_scenario()