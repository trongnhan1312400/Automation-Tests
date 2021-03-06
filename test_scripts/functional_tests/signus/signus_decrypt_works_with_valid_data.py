"""
Created on Dec 20, 2017

@author: nhan.nguyen
"""

import json

from indy import signus
from utilities import utils, constant, common
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestDecryptWithValidData(SignusTestBase):
    async def execute_precondition_steps(self):
        await super().execute_precondition_steps()
        common.delete_pool_folder(self.pool_name)

    async def execute_postcondition_steps(self):
        await super().execute_postcondition_steps()
        await common.close_and_delete_pool(self.pool_name, self.pool_handle)

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await \
            common.create_and_open_pool_ledger_for_steps(self.steps,
                                                         self.pool_name,
                                                         constant.
                                                         pool_genesis_txn_file)

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 5. Create 'my_did' and 'my_verkey'.
        self.steps.add_step("Create 'my_did' and 'my_verkey'")
        (my_did, my_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 6. Create 'their_did' and 'their_verkey'.
        self.steps.add_step("Create 'their_did' and 'their_verkey'")
        (their_did, their_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 7. Store 'their_did' and 'their_verkey' into wallet.
        self.steps.add_step("Store 'their_did' and 'their_verkey' into wallet")
        their_did_json = json.dumps({"did": their_did, "verkey": their_verkey})
        await utils.perform(self.steps, signus.store_their_did,
                            self.wallet_handle, their_did_json)

        # 8. Encrypte message by 'signus.encrypt'
        self.steps.add_step("Encrypte message by 'signus.encrypt'")
        message = "Test signus".encode("utf-8")
        (encrypted_message, nonce) = await \
            utils.perform(self.steps, signus.encrypt, self.wallet_handle,
                          self.pool_handle, my_did, their_did, message)

        # 9. Decrypt message by 'signus.decrypt'.
        self.steps.add_step("Decrypt message by 'signus.decrypt'")
        decrypted_msg = await utils.perform(self.steps, signus.decrypt,
                                            self.wallet_handle,
                                            self.pool_handle,
                                            my_did, their_did,
                                            encrypted_message, nonce)

        # 10. Check returned decrypted message.
        self.steps.add_step("Check returned decrypted message")
        error_message = "Decrypted message mismatches with message in step 8"
        utils.check(self.steps, error_message,
                    condition=lambda: decrypted_msg == message)


if __name__ == "__main__":
    TestDecryptWithValidData().execute_scenario()
