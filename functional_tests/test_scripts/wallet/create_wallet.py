"""
Created on Dec 08, 2017

@author: khoi.ngo
Implementing test case create_wallet with valid value.
"""
import os
from indy import wallet
from indy.error import IndyError
from libraries.constant import Constant, Colors
from libraries.common import Common
from libraries.utils import perform, exit_if_exception
from libraries.result import Status
from libraries.test_scenario_base import TestScenarioBase


class CreateWallet(TestScenarioBase):

    async def execute_postcondition_steps(self):
        Common().clean_up_pool_and_wallet_folder(self.pool_name, self.wallet_name)

    async def execute_test_steps(self):
        print("CreateWallet started")
        try:
            # 1. Create pool
            self.steps.add_step("Create pool Ledger")
            result = await perform(self.steps, Common.create_and_open_pool,
                                   self.pool_name, self.pool_genesis_txn_file)
            self.pool_handle = exit_if_exception(result)

            # 2. Create wallet
            self.steps.add_step("Create wallet")
            returned_code = await perform(self.steps, wallet.create_wallet, self.pool_name, self.wallet_name,
                                          None, None, None)

            # 3. Verify create wallet successfully
            self.steps.add_step("Verify wallet folder exist")
            wallet_path = Constant.work_dir + "/wallet/" + self.wallet_name
            result = os.path.exists(wallet_path)
            if (not isinstance(returned_code, IndyError)) and (result is True):
                self.steps.get_last_step().set_status(Status.PASSED)
            else:
                self.steps.get_last_step().set_message("Failed. Cannot find the wallet which was created.")
        except Exception as e:
            print(Colors.FAIL + "\n\t{}\n".format(str(e)) + Colors.ENDC)
        print("CreateWallet completed")


if __name__ == '__main__':
    CreateWallet().execute_scenario()
