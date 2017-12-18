"""
Created on Dec 18, 2017

@author: nhan.nguyen
"""

from indy import anoncreds
from utilities import utils, common
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverCreateMasterSecret(AnoncredsTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create master secret.
        self.steps.add_step("Create master secret")
        result = await utils.perform(self.steps,
                                     anoncreds.prover_create_master_secret,
                                     self.wallet_handle, "Test_anoncreds")

        # 4. Verify that None is returned.
        self.steps.add_step("Verify that None is returned")
        error_msg = "Cannot create master secret"
        utils.check(self.steps, error_msg,
                    condition=lambda: result is None)


if __name__ == '__main__':
    TestProverCreateMasterSecret().execute_scenario()
