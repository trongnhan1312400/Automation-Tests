"""
Created on Dec 12, 2017

@author: nhan.nguyen
"""

import json

from indy import signus, ledger
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestGetEndPointForDidFromLedger(SignusTestBase):
    async def execute_precondition_steps(self):
        await super().execute_precondition_steps()
        common.delete_pool_folder(self.pool_name)

    async def execute_postcondition_steps(self):
        await super().execute_postcondition_steps()
        await common.close_and_delete_pool(self.pool_name, self.pool_handle)

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file)

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 5. Create did and verkey with default trustee seed.
        self.steps.add_step("Create did and verkey with empty json")
        (my_did, my_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle,
                          json.dumps({"seed": constant.seed_default_trustee}))

        # 6. Build attribute request.
        self.steps.add_step("Build attribute request")
        ep_json = {"endpoint": {"ha": constant.endpoint, "verkey": my_verkey}}
        attr_req = await utils.perform(self.steps, ledger.build_attrib_request,
                                       my_did, my_did, None,
                                       json.dumps(ep_json), None)

        # 7. Sign and submit request to ledger.
        self.steps.add_step("Sign and submit request to ledger")
        await utils.perform(self.steps, ledger.sign_and_submit_request,
                            self.pool_handle, self.wallet_handle, my_did,
                            attr_req)

        # 8. Get end point of 'my_did'.
        self.steps.add_step("Get end point of 'my_did'")
        (returned_endpoint, returned_verkey) = await utils.perform(
            self.steps, signus.get_endpoint_for_did, self.wallet_handle,
            self.pool_handle, my_did)

        # 9. Check returned verkey.
        self.steps.add_step("Check returned verkey")
        error_msg = "Returned verkey mismatches with verkey that is set"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_verkey == my_verkey)

        # 10. Check returned endpoint.
        self.steps.add_step("Check returned endpoint")
        error_msg = "Returned endpoint mismatches with endpoint that is set"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_endpoint ==
                    ep_json['endpoint']['ha'])


if __name__ == "__main__":
    TestGetEndPointForDidFromLedger().execute_scenario()
