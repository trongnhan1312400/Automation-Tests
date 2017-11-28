'''
Created on Nov 28, 2017

@author: khoi.ngo
Implementing test case signus.py in the below link.
https://github.com/hyperledger/indy-sdk/blob/master/samples/python/src/ledger.py
'''

import json
import os.path
import sys
from indy import signus, wallet, pool, ledger
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from libraries.constant import Constant, Colors, Roles
from libraries.result import Status
from libraries.common import Common
from libraries.utils import *
from test_scripts.test_scenario_base import TestScenarioBase


class LedgerSample(TestScenarioBase):

    pool_name = generate_random_string("pool_test")
    my_wallet_name = generate_random_string("my_wallet")
    their_wallet_name = generate_random_string("their_wallet")
    pool_handle = 0
    my_wallet_handle = 0
    their_wallet_handle = 0

    async def execute_precondition_steps(self):
        """
        Clean up the pool and wallets folders without using lib-indy.
        """
        Common().clean_up_pool_and_wallet_folder(self.pool_name, self.my_wallet_name)
        Common().clean_up_pool_and_wallet_folder(self.pool_name, self.their_wallet_name)

    async def execute_postcondition_steps(self):
        """
        Closing my_wallet, their_wallet and pool. Then, deleting them.
        """
        # Close 2 wallets and the pool.
        await wallet.close_wallet(self.my_wallet_handle)
        await wallet.close_wallet(self.their_wallet_handle)
        await pool.close_pool_ledger(self.pool_handle)

        # Delete 2 wallets and the pool.
        await wallet.delete_wallet(self.their_wallet_name, None)
        await wallet.delete_wallet(self.my_wallet_name, None)
        await pool.delete_pool_ledger_config(self.pool_name)

    async def execute_test_steps(self):
        print("Ledger sample -> started")
        # 1. Create pool
        self.steps.add_step("Create pool Ledger")
        self.pool_handle = await perform(self.steps, Common.create_and_open_pool,
                                         self.pool_name, self.pool_genesis_txn_file)

        # 2. Create and open my wallet
        self.steps.add_step("Create and open my wallet")
        self.my_wallet_handle = await perform(self.steps, Common.create_and_open_wallet,
                                              self.pool_name, self.my_wallet_name)

        # 3. Create Their Wallet and Get Wallet Handle
        self.steps.add_step("Create their wallet and get wallet handle")
        self.their_wallet_handle = await perform(self.steps, Common.create_and_open_wallet,
                                                 self.pool_name, self.their_wallet_name)

        # 4. create my DID
        self.steps.add_step("Create my DID")
        (my_did, my_verkey) = await perform(self.steps, signus.create_and_store_my_did, self.my_wallet_handle, "{}")

        # 5. create their DID
        self.steps.add_step("Create their DID")
        (their_did, their_verkey) = await perform(self.steps, signus.create_and_store_my_did,
                                                  self.their_wallet_handle, json.dumps({"seed": Constant.seed_default_trustee}))

        # 6. Store Their DID
        self.steps.add_step("Store Their DID")
        their_identity_json = json.dumps({'did': their_did, 'verkey': their_verkey})
        await perform(self.steps, signus.store_their_did, self.my_wallet_handle, their_identity_json)

        # 7. Prepare and send NYM transaction
        self.steps.add_step("Prepare and send NYM transaction")
        await perform(self.steps, Common().build_and_send_nym_request, self.pool_handle,
                      self.their_wallet_handle, their_did, my_did, None, None, None)

        # 8. Prepare and send GET_NYM request
        self.steps.add_step("Prepare and send GET_NYM request")
        get_nym_txn_req8 = await perform(self.steps, ledger.build_get_nym_request, their_did, my_did)
        get_nym_txn_resp = await perform(self.steps, ledger.submit_request, self.pool_handle, get_nym_txn_req8)

        # 9. Verify GET_NYM request
        self.steps.add_step("Verify GET_NYM request")
        try:
            get_nym_txn_resp = json.loads(get_nym_txn_resp)
            if (get_nym_txn_resp['result']['dest'] == my_did):
                self.steps.get_last_step().set_status(Status.PASSED)
        except Exception as E:
            self.steps.get_last_step().set_message(str(E))

        print("Ledger sample -> completed")


if __name__ == '__main__':
    LedgerSample().execute_scenario()
