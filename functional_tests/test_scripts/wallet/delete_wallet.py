"""
Created on Dec 8, 2017

@author: khoi.ngo

Implementing test case DeleteWallet with valid value.
"""
from indy.error import ErrorCode
from indy import wallet
from libraries.test_scenario_base import TestScenarioBase
from libraries.utils import perform, exit_if_exception, perform_with_expected_code
from libraries.common import Common


class DeleteWallet(TestScenarioBase):

    async def execute_postcondition_steps(self):
        Common().clean_up_pool_and_wallet_folder(self.pool_name, self.wallet_name)

    async def execute_test_steps(self):
        print("DeleteWallet test started")
        # 1. Create and open a pool
        self.steps.add_step("Create and open a pool Ledger")
        result = await perform(self.steps, Common.create_and_open_pool,
                               self.pool_name, self.pool_genesis_txn_file)
        self.pool_handle = exit_if_exception(result)

        # 2. Create and open a wallet
        self.steps.add_step("Create and open wallet")
        self.wallet_handle = await perform(self.steps, Common.create_and_open_wallet,
                                           self.pool_name, self.wallet_name)

        # 3. Close wallet
        self.steps.add_step("Close wallet.")
        await perform(self.steps, wallet.close_wallet, self.wallet_handle)

        # 4. Delete wallet
        self.steps.add_step("Delete wallet.")
        await perform(self.steps, wallet.delete_wallet, self.wallet_name, None)

        # 5. Verify that user is able to delete a wallet by deleting that wallet twice.
        self.steps.add_step("Verify that user is able to delete a wallet.")
        assert await perform_with_expected_code(self.steps, wallet.delete_wallet, self.wallet_name, None,
                                                expected_code=ErrorCode.CommonIOError)
        print("DeleteWallet test completed")


if __name__ == '__main__':
    DeleteWallet().execute_scenario()
