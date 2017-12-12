"""
Created on Dec 12, 2017

@author: nhan.nguyen
"""

import json
from indy import signus
from libraries.common import Common
from libraries.constant import Constant
from libraries import utils
from test_scripts.signus.signus_test_base import SignusTestBase


class TestCreateDidWithPassedDid(SignusTestBase):

    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await Common.create_and_open_wallet_for_steps(self.steps, self.wallet_name, self.pool_name)

        # 3. Create did and verkey with passed did.
        self.steps.add_step("Create did and verkey with passed did")
        (my_did, _) = await utils.perform(self.steps, signus.create_and_store_my_did, self.wallet_handle,
                                          json.dumps({"did": Constant.did_my1}))

        # 4. Check created did.
        self.steps.add_step("Check created did")
        utils.check(self.steps, error_message="Created did is invalid",
                    condition=lambda: my_did == Constant.did_my1)


if __name__ == "__main__":
    TestCreateDidWithPassedDid().execute_scenario()
