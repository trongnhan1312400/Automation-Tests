"""
Created on Nov 8, 2017

@author: nhan.nguyen
"""

import json
import os.path
import sys
from indy import signus
from indy.error import IndyError
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.constant import Constant, Colors, Roles
from libraries.result import Status
from libraries.common import Common
from libraries.utils import *
from test_scripts.test_scenario_base import TestScenarioBase


class TestScenario04(TestScenarioBase):

    def __init__(self):
        super().__init__(total_steps=3, test_name="test_scenario_04_keyrings_wallet")

    async def execute_test_case(self):
        print("Test Scenario 04 -> started")
        seed_default_trustee = "000000000000000000000000Trustee1"
        try:
            # 1. Create and open pool Ledger  ---------------------------------------------------------
            self.steps[0].set_name("Create and open pool Ledger")
            returned_code = await perform(self.steps[0], Common.prepare_pool_and_wallet, self.pool_name,
                                          self.wallet_name, self.pool_genesis_txn_file)

            self.pool_handle, self.wallet_handle = raise_if_exception(returned_code)

            # 2. verify wallet was created in .indy/wallet
            self.steps[1].set_name("Verify wallet was created in .indy/wallet")
            wallet_path = Constant.work_dir + "/wallet/" + self.wallet_name
            result = os.path.exists(wallet_path)
            if result:
                self.steps[1].set_status(Status.PASSED)

            # 3. create DID to check the new wallet work well.
            self.steps[2].set_name("Create DID to check the new wallet work well")
            await perform(self.steps[2], signus.create_and_store_my_did,
                          self.wallet_handle, json.dumps({"seed": seed_default_trustee}))
        except IndyError as e:
            print(Colors.FAIL + "Stop due to IndyError: " + str(e) + Colors.ENDC)
        except Exception as ex:
            print(Colors.FAIL + "Exception: " + str(ex) + Colors.ENDC)

        print("Test Scenario 04 -> completed")


if __name__ == '__main__':
    TestScenario04().execute_scenario()
