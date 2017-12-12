"""
Created on Dec 12, 2017

@author: khoi.ngo

Implementing test case SchemaRequest with valid value.
"""
import json

from indy import signus, ledger

from libraries.common import Common
from libraries.constant import Constant
from libraries.result import Status
from libraries.test_scenario_base import TestScenarioBase
from libraries.utils import perform, compare_json


class SchemaRequest(TestScenarioBase):

    async def execute_test_steps(self):
        print("SchemaRequest started")
        # 1. Prepare pool and wallet. Get pool_hanlde, wallet_hanlde
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = await perform(self.steps, Common.prepare_pool_and_wallet,
                                                             self.pool_name, self.wallet_name, self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DID")
        (submitter_did, _) = await perform(self.steps, signus.create_and_store_my_did, self.wallet_handle,
                                           json.dumps({"seed": Constant.seed_default_trustee}))

        # 3. build schema request
        self.steps.add_step("Build schema request")
        data = '{"name":"name", "version":"1.0", "attr_names":["name","male"]}'
        response = json.loads(await perform(self.steps, ledger.build_schema_request, submitter_did, data))

        # 4. Verifying build schema successfully by checking data response
        self.steps.add_step("Verifying build schema successfully by checking data response")
        expected_response = {"operation": {"type": "101", "data": json.loads(data)}}
        try:
            assert compare_json(expected_response, response)
            self.steps.get_last_step().set_status(Status.PASSED)
        except AssertionError as e:
            self.steps.get_last_step().set_message("Failed. Json response is incorrect. " + str(e))
        print("SchemaRequest completed")


if __name__ == '__main__':
    SchemaRequest().execute_scenario()
