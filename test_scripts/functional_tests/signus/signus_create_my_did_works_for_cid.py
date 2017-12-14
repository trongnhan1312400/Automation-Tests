"""
Created on Dec 12, 2017

@author: nhan.nguyen
"""

import json
from indy import signus
from libraries.common import Common
from libraries.constant import Constant
from libraries import utils
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestCreateDidWithCid(SignusTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            Common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verkey with cid.
        self.steps.add_step("Create did and verkey with cid")
        (my_did, my_verkey) = await \
            utils.perform(self.steps,
                          signus.create_and_store_my_did, self.wallet_handle,
                          json.dumps({"seed": Constant.seed_my1, "cid": True}))

        # 4. Check created did.
        self.steps.add_step("Check created did")
        utils.check(self.steps, error_message="Created did is invalid",
                    condition=lambda: my_did == Constant.verkey_my1)

        # 5. Check created verkey.
        self.steps.add_step("Check created verkey")
        utils.check(self.steps, error_message="Created verkey is invalid",
                    condition=lambda: my_verkey == Constant.verkey_my1)


if __name__ == "__main__":
    TestCreateDidWithCid().execute_scenario()