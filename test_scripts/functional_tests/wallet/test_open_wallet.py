"""
Created on Dec 08, 2017

@author: khoi.ngo
Implementing test case open_wallet with valid value.
"""
import pytest
import os
import inspect
import time
from indy.error import IndyError
from utilities.test_scenario_base import TestScenarioBase
from utilities.utils import perform
from utilities import common, logger, result, step, utils, constant
from utilities.result import Status


class TestOpenWallet(TestScenarioBase):
    def setup_method(self):
        self.test_name = os.path.splitext(
            os.path.basename(inspect.getfile(self.__class__)))[0]

        self.test_result = result.Result(self.test_name)
        self.steps = step.Steps()
        self.logger = logger.Logger(self.test_name)
        self.pool_name = utils.generate_random_string("test_pool")
        self.wallet_name = utils.generate_random_string("test_wallet")
        self.pool_handle = None
        self.wallet_handle = None
        self.pool_genesis_txn_file = constant.pool_genesis_txn_file
        self.time_out = 300
        self.begin_time = time.time()

    @pytest.mark.asyncio
    async def test_open_wallet(self):
        print("OpenWallet test started")
        # 1. Create and open a pool
        self.steps.add_step("Create and open a pool")
        self.pool_handle = await perform(self.steps,
                                         common.create_and_open_pool,
                                         self.pool_name,
                                         self.pool_genesis_txn_file)

        # 2. Create and open a wallet
        self.steps.add_step("Create and open a wallet")
        returned_code = await perform(self.steps,
                                      common.create_and_open_wallet,
                                      self.pool_name, self.wallet_name)

        # 3. Verify that user is able to open a new wallet
        self.steps.add_step("Verify the response code of open_wallet API.")
        if not isinstance(returned_code, IndyError):
            self.wallet_handle = returned_code  # using for post-condition
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            self.steps.get_last_step().set_message(
                "Failed. Cannot open the wallet which was created.")

    async def temp(self):
        await common.clean_up_pool_and_wallet(self.pool_name,
                                        self.pool_handle,
                                        self.wallet_name,
                                        self.wallet_handle)

    def teardown_method(self):
        utils.run_async_method(self.temp)
        utils.make_final_result(self.test_result,
                                self.steps.get_list_step(),
                                self.begin_time, self.logger)
