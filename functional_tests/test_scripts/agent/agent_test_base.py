"""
Created on Dec 8, 2017

@author: nhan.nguyen

Containing a base class for agent testing.
"""

from indy import agent, signus
from indy import IndyError
from libraries.common import Common
from libraries.constant import Constant, Message
from libraries import utils
from libraries.result import Status
from libraries.test_scenario_base import TestScenarioBase


class AgentTestBase(TestScenarioBase):

    def __init__(self):
        super().__init__()
        self.message = "Test agent".encode("utf-8")
        self.sender_verkey = None
        self.recipient_verkey = Constant.vekey_my2
        self.encrypted_msg = None

    async def execute_precondition_steps(self):
        Common.delete_wallet_folder(self.wallet_name)

    async def execute_postcondition_steps(self):
        await Common.close_and_delete_wallet(self.wallet_name, self.wallet_handle)

    def execute_scenario(self, time_out=None):
        if self.__class__ is not AgentTestBase:
            super().execute_scenario(time_out)

    async def _check_encrypted_msg(self):
        if self.encrypted_msg is None or self.wallet_handle is None or self.recipient_verkey is None:
            return

        # Parse encrypted_message.
        self.steps.add_step("Verify 'parsed_message'")
        try:
            parsed_verkey, parsed_msg = await agent.parse_msg(self.wallet_handle, self.recipient_verkey,
                                                              self.encrypted_msg)
        except IndyError as ie:
            utils.print_error(Message.INDY_ERROR.format(str(ie)))
            self.steps.get_last_step().set_status(Status.FAILED)
            self.steps.get_last_step().set_message("Cannot parse encrypted message: {}".format(str(ie)))
            return

        # Verify parsed_message.
        if self.message is parsed_msg:
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            self.steps.get_last_step().set_status(Status.FAILED)
            self.steps.get_last_step().set_message("'parsed_message' mismatches with original 'message'")

        # Verify "parsed_verkey".
        if (self.sender_verkey is None and not parsed_verkey) or self.sender_verkey is parsed_verkey:
            self.steps.get_last_step().set_status(Status.PASSED)
        else:
            self.steps.get_last_step().set_status(Status.FAILED)
            self.steps.get_last_step().set_message("'parsed_verkey' mismatches with 'sender_verkey'")

    async def _create_and_open_wallet(self, wallet_name, pool_name) -> bool:
        # Create and open wallet.
        self.wallet_handle = await Common.create_and_open_wallet_for_steps(self.steps, wallet_name, pool_name)

        if isinstance(self.wallet_handle, Exception):
            self.wallet_handle = None
            return False

        return True

    async def _create_sender_verkey(self, wallet_handle, key_json):
        # Create 'sender_verkey'.
        self.steps.add_step("Create 'sender_verkey'")
        result = await utils.perform(self.steps, signus.create_key, wallet_handle, key_json)

        if not isinstance(result, Exception):
            self.sender_verkey = result

        return result

    async def _create_sender_verkey_with_did(self, wallet_handle, key_json):
        # Create 'sender_verkey' with "signus.create_and_store_my_did".
        self.steps.add_step("Create 'sender_verkey' with 'signus.create_and_store_my_did'")
        result = await utils.perform(self.steps, signus.create_and_store_my_did, wallet_handle, key_json)

        if not isinstance(result, Exception):
            (_, self.sender_verkey) = result

        return result

    async def _prepare_msg(self, wallet_handle, sender_verkey, recipient_verkey, msg):
        # Prepare message.
        self.steps.add_step("Prepare message")
        result = await utils.perform(self.steps, agent.prep_msg, wallet_handle, sender_verkey, recipient_verkey, msg)

        if not isinstance(result, Exception):
            self.encrypted_msg = result

        return result

    async def _prepare_anonymous_msg(self, recipient_verkey, msg):
        # Prepare anonymous message.
        self.steps.add_step("Prepare anonymous message")
        result = await utils.perform(self.steps, agent.prep_anonymous_msg, recipient_verkey, msg)

        if not isinstance(result, Exception):
            self.encrypted_msg = result

        return result
