"""
Created on Dec 8, 2017

@author: nhan.nguyen

Containing a base class for agent testing.
"""

from test_scripts.agent.agent_test_base import AgentTestBase


class TestAgentPrepMessageWithCreatedDid(AgentTestBase):

    async def execute_test_steps(self):
        # 1. Created wallet.
        # 2. Open wallet.
        if not await super()._create_and_open_wallet(self.wallet_name, self.pool_name):
            return

        # 3. Create "sender_verkey" with "signus.created_and_store_my_did".
        await super()._create_sender_verkey_with_did(self.wallet_handle, "{}")
        if not self.sender_verkey:
            return

        # 4. Prepare message.
        await super()._prepare_msg(self.wallet_handle, self.sender_verkey, self.recipient_verkey, self.message)
        if not self.encrypted_msg:
            return

        # 5. Parsed 'encrypted_message'.
        # 6. Check 'parsed_message'
        # 7. Check 'parsed_verkey'
        await super()._check_encrypted_msg()


if __name__ == "__main__":
    TestAgentPrepMessageWithCreatedDid().execute_scenario()
