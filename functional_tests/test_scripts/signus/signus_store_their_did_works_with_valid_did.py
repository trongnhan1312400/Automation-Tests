"""
Created on Dec 12, 2017

@author: nhan.nguyen
"""

import json
from indy import signus
from libraries.common import Common
from libraries import utils
from test_scripts.signus.signus_test_base import SignusTestBase


class TestStoreDidIntoWallet(SignusTestBase):

    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            Common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (their_did, _) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Store created did into wallet.
        result = await utils.perform(self.steps, signus.store_their_did,
                                     json.dumps({"did": their_did}))

        # 5. Verify that did is set successfully.




if __name__ == "__main__":
    TestStoreDidIntoWallet().execute_scenario()
