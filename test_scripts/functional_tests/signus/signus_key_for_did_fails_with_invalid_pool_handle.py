"""
Created on Dec 21, 2017

@author: nhan.nguyen
"""

from indy import signus
from indy.error import ErrorCode
from utilities import utils, common, constant
from test_scripts.functional_tests.signus.signus_test_base\
    import SignusTestBase


class TestKeyForDidWithInvalidPoolHandle(SignusTestBase):
    async def execute_precondition_steps(self):
        await super().execute_precondition_steps()
        common.delete_pool_folder(self.pool_name)

    async def execute_postcondition_steps(self):
        await super().execute_postcondition_steps()
        await common.close_and_delete_pool(self.pool_name, self.pool_handle)

    async def execute_test_steps(self):
        # 1. Create pool ledger config.
        # 2. Open pool ledger.
        self.pool_handle = await common.create_and_open_pool_ledger_for_steps(
            self.steps, self.pool_name, constant.pool_genesis_txn_file
        )

        # 3. Create wallet.
        # 4. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 5. Get verkey with invalid pool handle and
        # verify that user cannot get verkey.
        self.steps.add_step("Get verkey with invalid pool handle and "
                            "verify that user cannot get verkey")
        error_code = ErrorCode.PoolLedgerInvalidPoolHandle
        await utils.perform_with_expected_code(self.steps, signus.key_for_did,
                                               self.pool_handle + 1,
                                               self.wallet_handle,
                                               constant.did_my1,
                                               expected_code=error_code)


if __name__ == "__main__":
    TestKeyForDidWithInvalidPoolHandle().execute_scenario()
