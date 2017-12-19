"""
Created on Dec 13, 2017

@author: khoi.ngo

Implementing test case GetAttribRequest with valid value.
"""
import json

from indy import signus, ledger

from utilities import common
from utilities.constant import seed_default_trustee, get_attrib_response
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json


class GetAttribRequest(TestScenarioBase):

    async def execute_test_steps(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = await perform(
                                    self.steps, common.prepare_pool_and_wallet,
                                    self.pool_name, self.wallet_name,
                                    self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DIDs")
        (submitter_did, _) = await perform(
                                    self.steps,
                                    signus.create_and_store_my_did,
                                    self.wallet_handle,
                                    json.dumps({"seed": seed_default_trustee}))

        # 3. build attrib request
        self.steps.add_step("Create DIDs")
        raw = '{"endpoint":{"ha":"127.0.0.1:5555"}}'
        attrib_req = await perform(self.steps, ledger.build_attrib_request,
                                   submitter_did, submitter_did, None,
                                   raw, None)

        # 4. send attrib request
        self.steps.add_step("send attrib request")
        await perform(self.steps, ledger.sign_and_submit_request,
                      self.pool_handle, self.wallet_handle,
                      submitter_did, attrib_req)

        # 5.build a GET_ATTRIB request
        self.steps.add_step("build get attrib request")
        raw_name = "endpoint"
        get_attrib_req = json.loads(await perform(
                                self.steps, ledger.build_get_attrib_request,
                                submitter_did, submitter_did, raw_name))

        # 6. Verify json get schema request is correct.
        self.steps.add_step("Verify json get schema request is correct.")
        expected_response = json.loads(
            get_attrib_response.format(submitter_did, "104",
                                       submitter_did, json.dumps(raw_name)))
        verify_json(self.steps, expected_response, get_attrib_req)


if __name__ == '__main__':
    GetAttribRequest().execute_scenario()
