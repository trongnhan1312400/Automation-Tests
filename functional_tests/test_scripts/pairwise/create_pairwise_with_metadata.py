"""
Created on Dec 11, 2017

@author: nhan.nguyen
"""

from indy import signus, pairwise
from libraries.common import Common
from libraries.constant import Constant
from libraries import utils
from test_scripts.pairwise.pairwise_test_base import PairwiseTestBase


class TestCreatePairwiseWithMetadata(PairwiseTestBase):

    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await Common.create_and_open_wallet_for_steps(self.steps, self.wallet_name, self.pool_name)

        # 3. Create and store "my_did" by random seed.
        (my_did, _) = await 
