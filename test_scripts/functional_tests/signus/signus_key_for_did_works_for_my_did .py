"""
Created on Dec 21, 2017

@author: nhan.nguyen
"""

from indy import signus
from utilities import utils
from utilities import common
from test_scripts.functional_tests.signus.signus_test_base\
    import SignusTestBase


class TestKeyForLocalDidWithMyDid(SignusTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (my_did, my_verkey) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Get local verkey of 'my_did' from wallet.
        self.steps.add_step("Get local verkey of 'my_did' from wallet")
        returned_verkey = await utils.perform(self.steps,
                                              signus.key)


if __name__ == "__main__":
    TestKeyForLocalDidWithMyDid().execute_scenario()
