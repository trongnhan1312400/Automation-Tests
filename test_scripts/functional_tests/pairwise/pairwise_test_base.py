"""
Created on Dec 20, 2017

@author: nhan.nguyen

Containing a base class for pairwise testing.
"""

from utilities import common
from utilities.test_scenario_base import TestScenarioBase


class PairwiseTestBase(TestScenarioBase):
    def __init__(self):
        if self.__class__ is not PairwiseTestBase:
            super().__init__()

    async def execute_precondition_steps(self):
        common.delete_wallet_folder(self.wallet_name)

    async def execute_postcondition_steps(self):
        await common.close_and_delete_wallet(self.wallet_name,
                                             self.wallet_handle)

    def execute_scenario(self, time_out=None):
        if self.__class__ is not PairwiseTestBase:
            super().execute_scenario(time_out)
