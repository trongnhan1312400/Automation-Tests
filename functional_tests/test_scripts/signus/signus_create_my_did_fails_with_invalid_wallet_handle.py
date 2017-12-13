"""
Created on Dec 13, 2017

@author: nhan.nguyen
"""

from indy import signus
from indy.error import ErrorCode
from libraries.common import Common
from libraries import utils
from test_scripts.signus.signus_test_base import SignusTestBase


class TestCreateDidWithInvalidWalletHandle(SignusTestBase):

    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            Common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verify that cannot create did
        # with invalid wallet handle.
        self.steps.add_step("Create did and verify that cannot create "
                            "did with invalid wallet handle")
        expected_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               signus.create_and_store_my_did,
                                               self.wallet_handle, "{}",
                                               expected_code)


if __name__ == "__main__":
    TestCreateDidWithInvalidWalletHandle().execute_scenario()
