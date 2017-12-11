"""
Created on Dec 11, 2017

@author: nhan.nguyen

Containing a base class for pairwise testing.
"""

from indy import agent, signus
from libraries.common import Common
from libraries.constant import Constant
from libraries import utils
from libraries.result import Status
from libraries.test_scenario_base import TestScenarioBase


class PairwiseTestBase(TestScenarioBase):

    async def execute_precondition_steps(self):
        Common.delete_wallet_folder(self.wallet_name)

    async def execute_postcondition_steps(self):
        await Common.close_and_delete_wallet(self.wallet_name, self.wallet_handle)

    def execute_scenario(self, time_out=None):
        if self.__class__ is not PairwiseTestBase:
            super().execute_scenario(time_out)
