"""
Created on Dec 12, 2017

@author: khoi.ngo

Implementing test case GetSchemaRequest with valid value.
"""
import json

from indy import signus, ledger
import pytest

from utilities import common
from utilities.constant import json_template, schema_response, \
    seed_default_trustee
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform, verify_json, generate_random_string
from utilities.result import Status


class TestGetSchemaRequest(TestScenarioBase):
    @pytest.mark.asyncio
    async def test_valid_data(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps,
                          common.prepare_pool_and_wallet,
                          self.pool_name,
                          self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create DID")
        (submitter_did, _) = \
            await perform(self.steps,
                          signus.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({
                              "seed": seed_default_trustee}))
        (target_did, _) = await perform(self.steps,
                                        signus.create_and_store_my_did,
                                        self.wallet_handle,
                                        json.dumps({"seed": seed_trustee_2}))

        # 3. Prepare data to check and build get schema request
        self.steps.add_step("build get schema request")
        name = generate_random_string(size=4)
        version = "1.1.1"
        data = ('{"name":"%s", "version":"%s"}' % (name, version))
        get_schema_req = json.loads(
            await perform(self.steps, ledger.build_get_schema_request,
                          submitter_did,
                          target_did, data))

        # 4. Verify json get schema request is correct.
        self.steps.add_step("Verify json get schema request is correct.")
        schema_operation = schema_response.format("107", target_did,
                                                  data)
        expected_response = json_template(submitter_did, schema_operation)
        verify_json(self.steps, expected_response, get_schema_req)

    @pytest.mark.asyncio
    async def _test_send_wrong_data(self):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps,
                          common.prepare_pool_and_wallet,
                          self.pool_name,
                          self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        seed_trustee_2 = "000000000000000000000000Trustee2"
        self.steps.add_step("Create DID")
        (submitter_did, _) = \
            await perform(self.steps,
                          signus.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({"seed": seed_trustee_2}))
        (schema_did, _) = await perform(self.steps,
                                        signus.create_and_store_my_did,
                                        self.wallet_handle,
                                        json.dumps({
                                            "seed": seed_default_trustee}))
        # 3. build schema request
        self.steps.add_step("Build schema request")
        name = generate_random_string(size=4)
        version = "1.1.1"
        print("name request: " + name)
        data_request = (
            '{"name":"%s", "version":"%s", "attr_names":["name","male"]}' % (
                name, version))
        schema_req = await perform(self.steps, ledger.build_schema_request,
                                   submitter_did, data_request)

        # 4. send schema request
        self.steps.add_step("send schema request")
        await perform(self.steps, ledger.sign_and_submit_request,
                      self.pool_handle, self.wallet_handle,
                      submitter_did, schema_req)

        # 5. Prepare data to check and build get schema request
        self.steps.add_step("build get schema request")
        data_get_schema = ('{"name":"%s", "version":"%s"}' % (name, version))
        get_schema_req = await perform(self.steps,
                                       ledger.build_get_schema_request,
                                       submitter_did, schema_did,
                                       data_get_schema)

        # 6. send get_schema request
        self.steps.add_step("send get schema request")
        result = await perform(self.steps, ledger.sign_and_submit_request,
                               self.pool_handle, self.wallet_handle,
                               submitter_did, get_schema_req)

        print("\n: " + str(result) + "\n")

#         # 6. Verify json get schema request is correct.
#         self.steps.add_step("Verify json get schema request is correct.")
#         schema_operation = schema_response.format("107", target_did,
#                                                   data_response)
#         expected_response = json_template(submitter_did, schema_operation)
#         verify_json(self.steps, expected_response, get_schema_req)

    invalid_structure = "ErrorCode.CommonInvalidStructure"
    non_type = "'NoneType' object has no attribute 'encode'"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("submitter_did,schema_did,data,expected_result", [
        ("", "", '{"name":"valid_name", "version":"1abc.0"}',
         invalid_structure),
        ("", "", '{"name":"name!@##$%", "version":"1.1"}', invalid_structure),
        ("", "", '{"version":"1.1.0"}', invalid_structure),
        ("", "", '{"name":"valid_name", "version":"1.1", \
        "extra_field":"extra field"}', invalid_structure),
        ("", "", '{"name":"valid_name", "name":"other_name", "version":"1.1"}',
         invalid_structure),
        ("", None, '{"name":"valid_name", "version":"1.1"}', non_type),
        (None, "", '{"name":"valid_name", "version":"1.1"}', non_type),
        ("", "", '{"name":"128 characters", \
                    "version":"1321321321321231325456" \
                              "31213213616546545213212312.3121321321" \
                              "32132132132132123132132.13213131" \
                              "3213213213212132132213515.3135148766"}',
            invalid_structure),
        ("", "", '{}', invalid_structure),
    ])
    async def test_negative_cases(self, submitter_did, schema_did,
                                  data, expected_result):
        # 1. Prepare pool and wallet. Get pool_handle, wallet_handle
        self.steps.add_step("Prepare pool and wallet")
        self.pool_handle, self.wallet_handle = \
            await perform(self.steps,
                          common.prepare_pool_and_wallet,
                          self.pool_name,
                          self.wallet_name,
                          self.pool_genesis_txn_file)

        # 2. Create and store did
        self.steps.add_step("Create DIDs")
        if(submitter_did is not None):
            (submitter_did, _) = await perform(self.steps,
                                               signus.create_and_store_my_did,
                                               self.wallet_handle,
                                               json.dumps({
                                                "seed": seed_default_trustee}))
        if(schema_did is not None):
            seed_trustee_2 = "000000000000000000000000Trustee2"
            (schema_did, _) = await perform(self.steps,
                                            signus.create_and_store_my_did,
                                            self.wallet_handle,
                                            json.dumps({
                                                "seed": seed_trustee_2}))

        # 3. build get schema request
        self.steps.add_step("Build schema request")
        result = await perform(self.steps, ledger.build_get_schema_request,
                               submitter_did, schema_did, data,
                               ignore_exception=True)

        # 4. Verify result
        self.steps.add_step("Verify expected result: " + str(expected_result))
        print("result: " + str(result))
        print("expected: " + str(expected_result))
        if str(result) == expected_result:
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            err_msg = "%s doesn't equal %s" % (result, expected_result)
            self.steps.get_last_step().set_status(Status.FAILED, err_msg)
            assert False
