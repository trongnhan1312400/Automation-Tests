"""
Created on Nov 8, 2017

@author: nhan.nguyen
"""

import json
import os.path
import logging
from indy import signus


class TestScenario04(TestScenarioBase):
    
    def __init__(self):
        super(TestScenarioBase, self).__init__()

    async def execute_test_case(self):
        print("Test Scenario 04 -> started")
        seed_default_trustee = "000000000000000000000000Trustee1"
        try:
            # 1. Create and open pool Ledger  ---------------------------------------------------------
            self.steps[1].set_name("Create and open pool Ledger")
            returned_code = await perform(self.steps[1], Common.prepare_pool_and_wallet, self.pool_name,
                                   self.wallet_name, self.pool_genesis_txn_file)
    
            self.pool_handle, self.wallet_handle = raise_if_exception(returned_code)
    
            # 2. verify wallet was created in .indy/wallet
            self.steps[2].set_name("Verify wallet was created in .indy/wallet")
            wallet_path = Constant.work_dir + "/wallet/" + wallet_name
            result = os.path.exists(wallet_path)
            if result:
                self.steps[2].set_status(Status.PASSED)
    
            # 3. create DID to check the new wallet work well.
            self.steps[3].set_name("Create DID to check the new wallet work well")
            await perform(self.steps[3], signus.create_and_store_my_did,
                          wallet_handle, json.dumps({"seed": seed_default_trustee}))
        except IndyError as e:
            print(Colors.FAIL + "Indy error: " + str(e) + Colors.ENDC)
        except Exception as ex:
            print(Colors.FAIL + "Exception: " + str(ex) + Colors.ENDC)

        print("Test Scenario 04 -> completed")


if __name__ == '__main__':
    test_scenario = TestScenario04()
    test_scenario.execute_scenario()
