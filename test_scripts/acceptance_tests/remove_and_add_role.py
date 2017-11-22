"""
Created on Nov 8, 2017

@author: nhan.nguyen
"""
import json
import sys
import os
from indy import ledger, signus
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.constant import Constant, Colors, Roles
from libraries.result import Status
from libraries.common import Common
from libraries import utils
from test_scripts.test_scenario_base import TestScenarioBase


class TestScenario09(TestScenarioBase):

    def __init__(self):
        super().__init__(total_steps=29, test_name="test_scenario09_remove_and_add_role")

    async def execute_test_case(self):
        """
        This function is the main part of test script.
        There is a bug in this scenario (in step 22, 23 24) so we log a bug here.
        """
        # 1. Create and open wallet, pool ledger.
        step = 0
        self.steps[step].set_name("Create and open wallet, pool ledger")
        result = await utils.perform(self.steps[1], Common.prepare_pool_and_wallet,
                                     self.pool_name, self.wallet_name, Constant.pool_genesis_txn_file)
        utils.raise_if_exception(result)
        (self.pool_handle, self.wallet_handle) = result

        # 2. Create DIDs.
        step = 1
        self.steps[step].set_name("Create DIDs")

        (default_trustee_did, default_trustee_verkey) = None, None
        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({"seed": Constant.seed_default_trustee}))
        if len(result) == 2:
            (default_trustee_did, default_trustee_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (trustee1_did, trustee1_verkey) = None, None
        if len(result) == 2:
            (trustee1_did, trustee1_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (trustee2_did, trustee2_verkey) = None, None
        if len(result) == 2:
            (trustee2_did, trustee2_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (steward1_did, steward1_verkey) = None, None
        if len(result) == 2:
            (steward1_did, steward1_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (steward2_did, steward2_verkey) = None, None
        if len(result) == 2:
            (steward2_did, steward2_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (steward3_did, steward3_verkey) = None, None
        if len(result) == 2:
            (steward3_did, steward3_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (trustanchor1_did, trustanchor1_verkey) = None, None
        if len(result) == 2:
            (trustanchor1_did, trustanchor1_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (trustanchor2_did, trustanchor2_verkey) = None, None
        if len(result) == 2:
            (trustanchor2_did, trustanchor2_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (trustanchor3_did, trustanchor3_verkey) = None, None
        if len(result) == 2:
            (trustanchor3_did, trustanchor3_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (user1_did, user1_verkey) = None, None
        if len(result) == 2:
            (user1_did, user1_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (user3_did, user3_verkey) = None, None
        if len(result) == 2:
            (user3_did, user3_verkey) = result

        result = await utils.perform(self.steps[step], signus.create_and_store_my_did,
                                     self.wallet_handle, json.dumps({}))
        (user4_did, user4_verkey) = None, None
        if len(result) == 2:
            (user4_did, user4_verkey) = result

        # ==========================================================================================================
        # Test starts here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # ==========================================================================================================

        # 3. Using default Trustee to create Trustee1.
        step = 2
        self.steps[step].set_name("Using default Trustee to create Trustee1")
        await self.add_nym(self.steps[step], default_trustee_did, trustee1_did, trustee1_verkey, None, Roles.TRUSTEE)

        # 4. Verify GET NYM - Trustee1.
        step = 3
        self.steps[step].set_name("Verify GET NYM - Trustee1")
        await self.get_nym(self.steps[step], default_trustee_did, trustee1_did)

        # 5. Using Trustee1 to create Steward1.
        step = 4
        self.steps[step].set_name("Using Trustee1 to create Steward1")
        await self.add_nym(self.steps[step], trustee1_did, steward1_did, steward1_verkey, None, Roles.STEWARD)

        # 6. Verify GET NYM - Steward1.
        step = 5
        self.steps[step].set_name("Verify GET NYM - Steward1")
        await self.get_nym(self.steps[step], trustee1_did, steward1_did)

        # 7. Add identity (no role) by Trustee1.
        step = 6
        self.steps[step].set_name("Add identity (no role) by Trustee1")
        await self.add_nym(self.steps[step], trustee1_did, user3_did, user3_verkey, None, None)

        # 8. Verify GET NYM - no role.
        step = 7
        self.steps[step].set_name("Verify GET NYM - no role")
        await self.get_nym(self.steps[step], trustee1_did, user3_did)

        # Role TGB is not exist so we do not execute step 9.
        # 9. Using Trustee1 to create a TGB role.
        step = 8
        self.steps[step].set_name("Using Trustee1 to create a TGB role (SKIP)")
        self.steps[step].set_status(Status.PASSED)

        # Role TGB is not exist so we do not execute step 12.
        # 10. Verify GET NYM - TGB1.
        step = 9
        self.steps[step].set_name("Verify GET NYM - TGB1 (SKIP)")
        self.steps[step].set_status(Status.PASSED)

        # 11. Using Steward1 to create TrustAnchor1.
        step = 10
        self.steps[step].set_name("Using Steward1 to create TrustAnchor1")
        await self.add_nym(self.steps[step], steward1_did, trustanchor1_did, trustanchor1_verkey,
                           None, Roles.TRUST_ANCHOR)

        # 12. Verify GET NYM - TrustAnchor1.
        step = 11
        self.steps[step].set_name("Verify GET NYM - TrustAnchor1")
        await self.get_nym(self.steps[step], steward1_did, trustanchor1_did)

        # 13. Verify add identity (no role) by Steward1.
        step = 12
        self.steps[step].set_name("Verify add identity (no role) by Steward1")
        await self.add_nym(self.steps[step], steward1_did, user4_did, user4_verkey, None, None)

        # 14. Verify GET NYM.
        step = 13
        self.steps[step].set_name("Verify GET NYM - no role")
        await self.get_nym(self.steps[step], steward1_did, user4_did)

        # 15. Verify that a Steward cannot create another Steward.
        step = 14
        self.steps[step].set_name("Verify that Steward cannot create another Steward")
        (temp, message) = await self.add_nym(self.steps[step], steward1_did, steward2_did, steward2_verkey, None,
                                             Roles.STEWARD, error_code=304)

        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that a Steward cannot create a Steward!\n" + Colors.ENDC)
        else:
            if message is None:
                message = "Steward can create another Steward (should fail)"
            self.steps[step].set_message(message)

        # 16. Verify that a Steward cannot create a Trustee.
        step = 15
        self.steps[step].set_name("Verify that a Steward cannot create a Trustee")
        (temp, message) = await self.add_nym(self.steps[step], steward1_did, trustee1_did, trustee1_verkey,
                                             None, Roles.TRUSTEE, error_code=304)

        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that a Steward cannot create a Trustee!\n" + Colors.ENDC)
        else:
            if message is None:
                message = "Steward can create a Trustee (should fail)"
            self.steps[step].set_message(message)

        # 17. Using TrustAnchor1 to add a NYM.
        step = 16
        self.steps[step].set_name("Using TrustAnchor1 to add a NYM")
        await self.add_nym(self.steps[step], trustanchor1_did, user1_did, user1_verkey, None, None)

        # 18. Verify GET NYM - User1.
        step = 17
        self.steps[step].set_name("Verify GET NYM - User1")
        await self.get_nym(self.steps[step], trustanchor1_did, user1_did)

        # 19. Verify that TrustAnchor cannot create another TrustAnchor.
        step = 18
        self.steps[step].set_name("Verify that TrustAnchor cannot create another TrustAnchor")
        (temp, message) = await self.add_nym(self.steps[step], trustanchor1_did, trustanchor2_did, trustanchor2_verkey,
                                             None, Roles.TRUST_ANCHOR, error_code=304)
        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that a TrustAnchor cannot create another TrustAnchor!\n"
                  + Colors.ENDC)
        else:
            if message is None:
                message = "TrustAnchor can create another TrustAnchor (should fail)"
            self.steps[step].set_message(message)

        # 20. Using default Trustee to remove new roles.
        bug_is_430 = "Bug: https://jira.hyperledger.org/browse/IS-430"
        step = 19
        self.steps[step].set_name("Using default Trustee to remove new roles")
        message_20 = ""
        (temp, message) = await self.add_nym(self.steps[step], default_trustee_did, trustee1_did, trustee1_verkey,
                                             None, Roles.NONE)
        result = temp
        if not temp:
            message_20 += "\nCannot remove Trustee1's role - " + message
        else:
            (temp, message) = await self.get_nym(self.steps[step], default_trustee_did, trustee1_did)
            if not temp:
                message_20 += "\nCannot check self.get_nym for Trustee1 - " + message
            else:
                if not TestScenario09.check_role_in_retrieved_nym(message, Roles.NONE):
                    temp = False
                    message_20 += "\nCannot remove Trustee1's role"

        result = result and temp
        (temp, message) = await self.add_nym(self.steps[step], default_trustee_did, steward1_did, steward1_verkey,
                                             None, Roles.NONE)
        result = result and temp
        if not temp:
            message_20 += "\nCannot remove Steward1's role - " + message
        else:
            (temp, message) = await self.get_nym(self.steps[step], default_trustee_did, steward1_did)
            if not temp:
                message_20 += "\nCannot check self.get_nym for Steward1 - " + message
            else:
                if not TestScenario09.check_role_in_retrieved_nym(message, Roles.NONE):
                    temp = False
                    message_20 += "\nCannot remove Steward1's role"

        result = result and temp

        # Any step that involve to role TGB is skipped because role TGB is not supported by libindy
        # (temp, message) = await self.add_nym(default_trustee_did, tgb1_did,
        #                                       tgb1_verkey, None, Roles.NONE, can_add=True)
        # self.test_results["Step 22"] = self.test_results["Step 22"] and temp
        # if not temp:
        #     message_20 += "\nCannot remove TGB's role - " + message
        # else:
        #     (temp, message) = await self.get_nym(default_trustee_did, tgb1_did)
        #     if not temp:
        #         message_20 += "\nCannot check self.get_nym for TGB - " + message
        #     else:
        #         if not TestScenario09.check_role_in_retrieved_nym(message, Roles.NONE):
        #             temp = False
        #             message_20 += "\nCannot remove TGB1's role"
        #
        # self.test_results["Step 22"] = self.test_results["Step 22"] and temp

        (temp, message) = await self.add_nym(self.steps[step], default_trustee_did, trustanchor1_did,
                                             trustanchor1_verkey, None, Roles.NONE)
        result = result and temp

        if not temp:
            message_20 += "\nCannot remove Trust_Anchor1's role - " + message
        else:
            (temp, message) = await self.get_nym(self.steps[step], default_trustee_did, trustanchor1_did)
            if not temp:
                message_20 += "\nCannot check self.get_nym for Trust_Anchor1 - " + message
            else:
                if not TestScenario09.check_role_in_retrieved_nym(message, Roles.NONE):
                    temp = False
                    message_20 += "\nCannot remove Trust_Anchor1's role"

        result = result and temp

        if not result:
            self.steps[step].set_message("{}\n{}".format(message_20[1:], bug_is_430))
            self.steps[step].set_status(Status.FAILED)
        else:
            self.steps[step].set_status(Status.PASSED)

        # 21. Verify that removed Trustee1 cannot create Trustee or Steward.
        step = 20
        self.steps[step].set_name("Verify that removed Trustee1 cannot create Trustee or Steward")
        message_21 = ""
        (temp, message) = await self.add_nym(self.steps[step], trustee1_did, trustee2_did, trustee2_verkey,
                                             None, Roles.TRUSTEE, error_code=304)
        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that removed Trustee1 cannot create another Trustee!\n"
                  + Colors.ENDC)
        else:
            if message is None:
                message = ""
            message_21 += "\nRemoved Trustee can create Trustee (should fail) " + message

        result = temp

        (temp, message) = await self.add_nym(self.steps[step], trustee1_did, steward2_did, steward2_verkey,
                                             None, Roles.STEWARD, error_code=304)
        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that removed Trustee1 cannot create a Steward!\n" + Colors.ENDC)
        else:
            if message is None:
                message = ""
            message_21 += "\nRemoved Trustee can create Steward(should fail) " + message

        result = result and temp

        if not result:
            self.steps[step].set_message("{}\n{}".format(message_21[1:], bug_is_430))
            self.steps[step].set_status(Status.FAILED)
        else:
            self.steps[step].set_status(Status.PASSED)

        # 22. Verify that removed Steward1 cannot create TrustAnchor.
        step = 21
        self.steps[step].set_name("Verify that removed Steward1 cannot create TrustAnchor")
        (temp, message) = await self.add_nym(self.steps[step], steward1_did, trustanchor2_did, trustanchor2_verkey,
                                             None, Roles.TRUST_ANCHOR, error_code=304)
        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that removed Steward1 cannot create a TrustAnchor!\n"
                  + Colors.ENDC)
        else:
            if message is None:
                message = "Steward1 can create a TrustAnchor (should fail)"
            self.steps[step].set_message("{}\n{}".format(message, bug_is_430))

        # 23. Using default Trustee to create Trustee1.
        step = 22
        self.steps[step].set_name("Using default Trustee to create Trustee1")
        await self.add_nym(self.steps[step], default_trustee_did, trustee1_did, trustee1_verkey, None, Roles.TRUSTEE)

        # 24. Using Trustee1 to add Steward1 and TGB1.
        step = 23
        self.steps[step].set_name("Using Trustee1 to add Steward1 and TGB1")
        await self.add_nym(self.steps[step], trustee1_did, steward1_did, steward1_verkey, None, Roles.STEWARD)

        # Role TGB is not exist so we do not execute this step
        # (temp, message) = await self.add_nym(trustee1_did, tgb1_did, tgb1_verkey, None, Roles.TGB, can_add=True)
        # self.test_results["Step 26"] = self.test_results["Step 26"] and temp
        # if not temp:
        #     message_26 += "\nCannot use Trustee1 to add TGB1 - " + message

        # 25. Verify that Steward1 cannot add back a TrustAnchor removed by TrustTee.
        step = 24
        self.steps[step].set_name("Verify that Steward1 cannot add back a TrustAnchor removed by TrustTee")
        (temp, message) = await self.add_nym(self.steps[step], steward1_did, trustanchor1_did, trustanchor1_verkey,
                                             None, Roles.TRUST_ANCHOR, error_code=304)
        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that Steward1 cannot add "
                                   "back a TrustAnchor removed by TrustTee!\n"
                  + Colors.ENDC)
        else:
            if message is None:
                message = "Steward1 can add back TrustAnchor removed by Trustee (should fail)"
            self.steps[step].set_message(message)

        # 26. Verify that Steward cannot remove a Trustee.
        step = 25
        self.steps[step].set_name("Verify that Steward cannot remove a Trustee")
        (temp, message) = await self.add_nym(self.steps[step], steward1_did, trustee1_did,
                                             trustee1_verkey, None, Roles.NONE, error_code=304)
        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that Steward cannot remove a Trustee!\n" + Colors.ENDC)
        else:
            if message is None:
                message = "Steward can create a Trustee (should fail)"
            self.steps[step].set_message(message)

        # 27. Verify that Trustee can add new Steward.
        step = 26
        self.steps[step].set_name("Verify that Trustee can add new Steward")
        message_27 = ""
        (temp, message) = await self.add_nym(self.steps[step], trustee1_did, steward2_did,
                                             steward2_verkey, None, Roles.STEWARD)
        result = temp
        if not temp:
            message_27 += "\nTrustee cannot add Steward1 (should pass) - " + message

        (temp, message) = await self.add_nym(self.steps[step], trustee1_did, steward3_did,
                                             steward3_verkey, None, Roles.STEWARD)
        result = result and temp
        if not temp:
            message_27 += "\nTrustee cannot add Steward2 (should pass) - " + message

        if not result:
            self.steps[step].set_status(Status.FAILED)
            self.steps[step].set_message(message_27[1:])
        else:
            self.steps[step].set_status(Status.PASSED)

        # 28. Verify that Steward cannot remove another Steward.
        step = 27
        self.steps[step].set_name("Verify that Steward cannot remove another Steward")
        (temp, message) = await self.add_nym(self.steps[step], steward1_did, steward2_did,
                                             steward2_verkey, None, Roles.NONE, error_code=304)
        if temp:
            print(Colors.OKGREEN + "::PASS::Validated that Steward cannot remove another Steward!\n" + Colors.ENDC)
        else:
            if message is None:
                message = "Steward can remove another Steward (should fail)"
                self.steps[step].set_message(message)

        # 29. Verify Steward can add a TrustAnchor.
        step = 28
        self.steps[step].set_name("Verify Steward can add a TrustAnchor")
        await self.add_nym(self.steps[step], steward2_did, trustanchor3_did, trustanchor3_verkey,
                           None, Roles.TRUST_ANCHOR)

    async def add_nym(self, step, submitter_did, target_did, ver_key, alias, role, error_code=None):
        """
        Build a send NYM request and submit it.
        :param step:
        :param submitter_did:
        :param target_did:
        :param ver_key:
        :param alias:
        :param role:
        :param error_code:
        :return:
        """
        nym = await utils.perform(step, ledger.build_nym_request, submitter_did, target_did, ver_key, alias, role)
        if isinstance(nym, IndexError or Exception):
            return False, None

        if not error_code:
            result = await utils.perform(step, ledger.sign_and_submit_request, self.pool_handle,
                                         self.wallet_handle, submitter_did, nym)
            if isinstance(result, IndexError or Exception):
                return False, result
            return True, None
        else:
            result = await utils.perform_with_expected_code(step, ledger.sign_and_submit_request, self.pool_handle,
                                                            self.wallet_handle, submitter_did, nym,
                                                            expected_code=error_code)
            if step.get_status() == Status.FAILED:
                return False, result
            return True, None

    async def get_nym(self, step, submitter_did, target_did):
        """
        Build and submit GET NYM request.
        :param step:
        :param submitter_did:
        :param target_did:
        :return:
        """

        nym = await utils.perform(step, ledger.build_get_nym_request, submitter_did, target_did)
        if isinstance(nym, IndexError or Exception):
            return False, None
        result = await  utils.perform(step, ledger.submit_request, self.pool_handle, nym)
        if isinstance(result, IndexError or Exception):
            return False, result
        return True, result

    @staticmethod
    def check_role_in_retrieved_nym(retrieved_nym, role):
        """
        Check if the role in the GET NYM response is what we want.

        :param retrieved_nym:
        :param role: the role we want to check.
        :return: True if the role is what we want.
                 False if the role is not what we want.
        """
        if retrieved_nym is None:
            return False
        nym_dict = json.loads(retrieved_nym)
        if "data" in nym_dict["result"]:
            temp_dict = json.loads(nym_dict["result"]["data"])
            if "role" in temp_dict:
                if not temp_dict["role"] == role:
                    return False
                else:
                    return True
        return False


if __name__ == '__main__':
    TestScenario09().execute_scenario()
