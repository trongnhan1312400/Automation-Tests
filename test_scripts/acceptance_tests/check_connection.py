"""
Created on Nov 10, 2017

@author: nhan.nguyen
"""

import json
import sys
import os
from indy import pool, signus, wallet
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.constant import Constant
from libraries.utils import *
from test_scripts.test_scenario_base import TestScenarioBase


class TestScenario03(TestScenarioBase):
    seed_steward01 = "000000000000000000000000Steward1"

    def __init__(self):
        super().__init__(total_steps=8, test_name="test_scenario_03_check_connection")

    async def execute_test_case(self):
        pool_config = json.dumps({"genesis_txn": str(Constant.pool_genesis_txn_file)})
        # 1. Create pool ledger
        self.steps[1].set_name("Create pool ledger")
        await perform(self.steps[1], pool.create_pool_ledger_config, self.pool_name, pool_config)

        # 2. Create wallet
        self.steps[2].set_name("Create wallet")
        await perform(self.steps[2], wallet.create_wallet, self.pool_name, self.wallet_name, None, None, None)
        self.wallet_handle = await perform(self.steps[2], wallet.open_wallet, self.wallet_name, None, None)

        # 3. Create DID
        self.steps[3].set_name("Create DID")
        await perform(self.steps[3], signus.create_and_store_my_did,
                      self.wallet_handle, json.dumps({"seed": self.seed_steward01}))

        # 4. Connect to pool.
        # Verify that the default wallet move to Test from NoEnv?
        # Cannot verify because ".indy/wallet" do not include any folder that name
        # no-env and test, and default wallet cannot be created via indy-sdk
        self.steps[4].set_name("Connect to pool")
        self.pool_handle = await perform(self.steps[4], pool.open_pool_ledger, self.pool_name, None)

        # 5. Disconnect from pool.
        self.steps[5].set_name("Disconnect form pool")
        await perform(self.steps[5], pool.close_pool_ledger, self.pool_handle)

        # 6. Reconnect to pool.
        self.steps[6].set_name("Reconnect to pool")
        self.pool_handle = await perform(self.steps[6], pool.open_pool_ledger, self.pool_name, None)


if __name__ == '__main__':
    TestScenario03().execute_scenario()
