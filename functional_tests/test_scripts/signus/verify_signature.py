'''
Created on Nov 27, 2017

@author: khoi.ngo
Implementing test case signus.py in the below link.
https://github.com/hyperledger/indy-sdk/blob/master/samples/python/src/signus.py
'''

import json
import os.path
import sys
from indy import signus, wallet, pool
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from libraries.constant import Constant
from libraries.common import Common
from libraries.utils import *
from libraries.test_scenario_base import TestScenarioBase


class SignusSample(TestScenarioBase):

    my_wallet_name = generate_random_string("my_wallet")
    my_wallet_handle = 0
    their_wallet_name = generate_random_string("their_wallet")
    their_wallet_handle = 0
    pool_name = generate_random_string("pool_test")
    pool_handle = 0

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
        await wallet.close_wallet(self.my_wallet_handle)
        await wallet.close_wallet(self.their_wallet_handle)
        await wallet.delete_wallet(self.their_wallet_name, None)
        await wallet.delete_wallet(self.my_wallet_name, None)
        await pool.close_pool_ledger(self.pool_handle)
        await pool.delete_pool_ledger_config(self.pool_name)

    async def execute_test_steps(self):
        print("Signus sample -> started")
        # 1. Create pool
        self.steps.add_step("Create pool Ledger")
        result = await perform(self.steps, Common.create_and_open_pool,
                               self.pool_name, self.pool_genesis_txn_file)
        self.pool_handle = exit_if_exception(result)

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
        await perform(self.steps, signus.create_and_store_my_did, self.my_wallet_handle, "{}")

        # 5. create their DID
        self.steps.add_step("Create their DID")
        (their_did, their_verkey) = await perform(self.steps, signus.create_and_store_my_did,
                                                  self.their_wallet_handle, json.dumps({"seed": Constant.seed_default_trustee}))

        # 6. Store Their DID
        self.steps.add_step("Store Their DID")
        their_identity_json = json.dumps({'did': their_did, 'verkey': their_verkey})
        await perform(self.steps, signus.store_their_did, self.my_wallet_handle, their_identity_json)

        # 7. Their sign message
        self.steps.add_step("Their sign message")
        message = json.dumps({
            "reqId": 1495034346617224651,
            "identifier": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL",
            "operation": {
                "type": "1",
                "dest": "4efZu2SXufS556yss7W5k6Po37jt4371RM4whbPKBKdB"
            }
        })
        signature = await perform(self.steps, signus.sign, self.their_wallet_handle, their_did, message)

        # 8. Verify signature
        self.steps.add_step("Verify signature")
        assert await perform(self.steps, signus.verify_signature, self.my_wallet_handle, self.pool_handle, their_did, message, signature)

        print("Signus sample -> completed")


if __name__ == '__main__':
    SignusSample().execute_scenario()
