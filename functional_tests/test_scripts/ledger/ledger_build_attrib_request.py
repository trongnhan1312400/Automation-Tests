"""
Created on Dec 13, 2017

@author: khoi.ngo

Implementing test case BuildAttribRequest with valid value.
"""
import json

from indy import signus, ledger

from libraries.common import Common
from libraries.constant import Constant, JsonTemplate
from libraries.test_scenario_base import TestScenarioBase
from libraries.utils import perform, verify_json


class BuildAttribRequest(TestScenarioBase):

    async def execute_test_steps(self):
        # 1. Prepare pool and wallet. Get pool_hanlde, wallet_hanlde
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = await perform(self.steps, Common.prepare_pool_and_wallet,
                                                             self.pool_name, self.wallet_name, self.pool_genesis_txn_file)

        # 2. Create and store did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create DIDs")
        (submitter_did, _) = await perform(self.steps, signus.create_and_store_my_did, self.wallet_handle,
                                           json.dumps({"seed": Constant.seed_default_trustee}))
        (target_did, _) = await perform(self.steps, signus.create_and_store_my_did, self.wallet_handle,
                                        json.dumps({"seed": seed_trustee_2}))

        # 3. build attrib request
        self.steps.add_step("Create DIDs")
        raw = '{"endpoint":{"ha":"127.0.0.1:5555"}}'
        attib_req = json.loads(await perform(self.steps, ledger.build_attrib_request,
                                             submitter_did, target_did, None, raw, None))

        # 4. Verifying build_attrib_request json.
        self.steps.add_step("Verifying get_nym_request json")
        expected_response = json.loads(JsonTemplate.attrib_request.format(submitter_did, "100",
                                                                          target_did, json.dumps(raw)))
        verify_json(self.steps, expected_response, attib_req)


if __name__ == '__main__':
    BuildAttribRequest().execute_scenario()
