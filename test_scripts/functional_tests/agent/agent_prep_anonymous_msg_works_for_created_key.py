"""
Created on Dec 11, 2017

@author: nhan.nguyen
"""

from indy import agent
from libraries import utils
from test_scripts.agent.agent_test_base import AgentTestBase


class TestAgentPrepAnonymousMessage(AgentTestBase):

    async def execute_test_steps(self):
        # 1. Prepare anonymous message.
        self.steps.add_step("Prepare anonymous message")
        self.encrypted_msg = await utils.perform(self.steps, agent.prep_anonymous_msg, self.recipient_verkey,
                                                 self.message, ignore_exception=False)

        # 2. Parsed 'encrypted_message'.
        # 3. Check 'parsed_message'
        # 4. Check 'parsed_verkey'
        await super()._parsed_and_check_encrypted_msg()


if __name__ == "__main__":
    TestAgentPrepAnonymousMessage().execute_scenario()
