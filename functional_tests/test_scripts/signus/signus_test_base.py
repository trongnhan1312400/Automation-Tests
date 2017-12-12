"""
Created on Dec 12, 2017

@author: nhan.nguyen

Containing a base class for signus testing.
"""

from libraries.common import Common
from libraries.test_scenario_base import TestScenarioBase


class SignusTestBase(TestScenarioBase):

    async def execute_precondition_steps(self):
        Common.delete_wallet_folder(self.wallet_name)

    async def execute_postcondition_steps(self):
        await Common.close_and_delete_wallet(self.wallet_name, self.wallet_handle)

    def execute_scenario(self, time_out=None):
        if self.__class__ is not SignusTestBase:
            super().execute_scenario(time_out)
