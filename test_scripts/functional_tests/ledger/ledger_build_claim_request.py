"""
Created on Dec 19, 2017

@author: khoi.ngo

Implementing test case ClaimRequest with valid value.
"""
import json

from indy import signus, ledger

from utilities import common, constant
from utilities.result import Status
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform


class ClaimRequest(TestScenarioBase):

    async def execute_test_steps(self):
        # 1. Prepare pool and wallet. Get pool_hanlde, wallet_hanlde
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = await \
            perform(self.steps, common.prepare_pool_and_wallet, self.pool_name,
                    self.wallet_name, self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DIDs")
        (submitter_did, _) = await perform(
            self.steps, signus.create_and_store_my_did, self.wallet_handle,
            json.dumps({"seed": constant.seed_default_trustee}))


if __name__ == '__main__':
    ClaimRequest().execute_scenario()
