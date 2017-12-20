"""
Created on Dec 20, 2017

@author: nhan.nguyen
"""

import json
from indy import signus, pairwise
from utilities import utils, constant, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestCreatePairwiseWithMetadata(PairwiseTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create and store 'my_did' by random seed.
        self.steps.add_step("Create and store 'my_did' by random seed")
        (my_did, _) = await utils.perform(self.steps,
                                          signus.create_and_store_my_did,
                                          self.wallet_handle,
                                          "{}", ignore_exception=False)

        # 4. Create and "their_did" by default seed trustee.
        self.steps.add_step("Create 'their_did' by default seed trustee")
        (their_did, _) = await  utils.perform(
            self.steps, signus.create_and_store_my_did, self.wallet_handle,
            json.dumps({"seed": constant.seed_default_trustee}),
            ignore_exception=False)

        # 5. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, signus.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did}),
                            ignore_exception=False)

        # 6. Create pairwise.
        self.steps.add_step("Creare pairwise between 'my_did' and 'their_did'")
        metadata = "Test create pairwise"
        await utils.perform(self.steps, pairwise.create_pairwise,
                            self.wallet_handle, their_did, my_did, metadata)

        # 7 Get created pairwise.
        self.steps.add_step("Get created pairwise")
        pairwise_with_metadata = await utils.perform(self.steps,
                                                     pairwise.get_pairwise,
                                                     self.wallet_handle,
                                                     their_did)

        # 8. Verify 'pairwise_with_metadata'.
        self.steps.add_step("Verify 'pairwise_with_metadata'")
        utils.check(self.steps, error_message="Gotten pairwise mismatches",
                    condition=lambda: json.loads(pairwise_with_metadata) == {
                        "my_did": my_did, "metadata": metadata})


if __name__ == "__main__":
    TestCreatePairwiseWithMetadata().execute_scenario()
