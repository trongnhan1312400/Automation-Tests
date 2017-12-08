"""
Created on Dec 08, 2017

@author: khoi.ngo
Implementing test case open_wallet with valid value.
"""
from indy.error import IndyError
from libraries.test_scenario_base import TestScenarioBase
from libraries.utils import perform, exit_if_exception
from libraries.common import Common
from libraries.result import Status


class OpenWallet(TestScenarioBase):

    async def execute_test_steps(self):
        print("OpenWallet started")
        # 1. Create pool
        self.steps.add_step("Create pool Ledger")
        result = await perform(self.steps, Common.create_and_open_pool,
                               self.pool_name, self.pool_genesis_txn_file)
        self.pool_handle = exit_if_exception(result)

        # 2. Create wallet
        self.steps.add_step("Create and open wallet")
        returned_code = await perform(self.steps, Common.create_and_open_wallet,
                                      self.pool_name, self.wallet_name)

        # 3. Verify open wallet successfully
        self.steps.add_step("Verify the response code of open_wallet API.")
        if (not isinstance(returned_code, IndyError)):
            self.wallet_handle = returned_code  # using for post-condition
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            self.steps.get_last_step().set_message("Failed. Cannot open the wallet which was created.")

        print("OpenWallet completed")


if __name__ == '__main__':
    OpenWallet().execute_scenario()
