"""
Created on Nov 8, 2017

@author: khoi.ngo
"""

# /usr/bin/env python3.6
import sys
import json
import os
from indy import ledger, signus
from indy.error import IndyError
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.constant import Constant, Colors, Roles
from libraries.common import Common
from libraries.utils import *
from test_scripts.test_scenario_base import TestScenarioBase


# -----------------------------------------------------------------------------------------
# This will run acceptance tests that will validate the add/remove roles functionality.
# -----------------------------------------------------------------------------------------


class TestScenario11(TestScenarioBase):

    def __init__(self):
        super().__init__(total_steps=18, test_name="test_scenario_11_special_case_trust_anchor_role")

    async def execute_test_case(self):
        print("Test Scenario 11 -> started")
        # Declare all values use in the test
        seed_trustee1 = generate_random_string(prefix="Trustee1", size=32)
        seed_trustee2 = generate_random_string(prefix="Trustee2", size=32)
        seed_steward1 = generate_random_string(prefix="Steward1", size=32)
        seed_steward2 = generate_random_string(prefix="Steward2", size=32)
        seed_trustanchor1 = generate_random_string(prefix="TrustAnchor1", size=32)
        seed_trustanchor2 = generate_random_string(prefix="TrustAnchor2", size=32)
        seed_trustanchor3 = generate_random_string(prefix="TrustAnchor3", size=32)
        try:
            # 1. Create ledger config from genesis txn file  ---------------------------------------------------------
            self.steps[1].set_name("Create and open pool Ledger")
            result = await perform(self.steps[1], Common.prepare_pool_and_wallet, self.pool_name,
                                   self.wallet_name, self.pool_genesis_txn_file)

            self.pool_handle, self.wallet_handle = raise_if_exception(result)

            # 2. Create DIDs ----------------------------------------------------
            self.steps[2].set_name("Create DIDs")
            (default_trustee_did, default_trustee_verkey) = await perform(self.steps[2], signus.create_and_store_my_did,
                                                                          self.wallet_handle, json.dumps({"seed": Constant.seed_default_trustee}))

            (trustee1_did, trustee1_verkey) = await perform(self.steps[2], signus.create_and_store_my_did,
                                                            self.wallet_handle, json.dumps({"seed": seed_trustee1}))
            (trustee2_did, trustee2_verkey) = await perform(self.steps[2], signus.create_and_store_my_did,
                                                            self.wallet_handle, json.dumps({"seed": seed_trustee2}))
            (steward1_did, steward1_verkey) = await perform(self.steps[2], signus.create_and_store_my_did,
                                                            self.wallet_handle, json.dumps({"seed": seed_steward1}))
            (steward2_did, steward2_verkey) = await perform(self.steps[2], signus.create_and_store_my_did,
                                                            self.wallet_handle, json.dumps({"seed": seed_steward2}))
            (trustanchor1_did, trustanchor1_verkey) = await perform(self.steps[2], signus.create_and_store_my_did,
                                                                    self.wallet_handle, json.dumps({"seed": seed_trustanchor1}))
            (trustanchor2_did, trustanchor2_verkey) = await perform(self.steps[2], signus.create_and_store_my_did,
                                                                    self.wallet_handle, json.dumps({"seed": seed_trustanchor2}))
            (trustanchor3_did, trustanchor3_verkey) = await perform(self.steps[2], signus.create_and_store_my_did,
                                                                    self.wallet_handle, json.dumps({"seed": seed_trustanchor3}))

            # 3. Using the default Trustee create a TrustAnchor and a new Trustee---------------
            self.steps[3].set_name("Use default Trustee to create a Trustee")
            nym_txn_req3 = await perform(self.steps[3], ledger.build_nym_request, default_trustee_did, trustee1_did,
                                         trustee1_verkey, None, Roles.TRUSTEE)
            await perform(self.steps[3], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                          default_trustee_did, nym_txn_req3)

            # 4. Verify GET_NYM for trustee1-----------------------------------------------------------------------------------
            self.steps[4].set_name("Verify get nym for Trustee")
            get_nym_txn_req4 = await perform(self.steps[4], ledger.build_get_nym_request, default_trustee_did, trustee1_did)
            await perform(self.steps[4], ledger.submit_request, self.pool_handle, get_nym_txn_req4)

            # 5. Create TrustAnchor1
            self.steps[5].set_name("Create TrustAnchor1")
            nym_txn_req5 = await perform(self.steps[5], ledger.build_nym_request, default_trustee_did, trustanchor1_did,
                                         trustanchor1_verkey, None, Roles.TRUST_ANCHOR)
            await perform(self.steps[5], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                          default_trustee_did, nym_txn_req5)

            # 6. Verify GET_NYM for TrustAnchor1-------------------------------------------------------------------------------
            self.steps[6].set_name("Verify GET_NYM for TrustAnchor1")
            get_nym_txn_req6 = await perform(self.steps[6], ledger.build_get_nym_request, default_trustee_did, trustanchor1_did)
            await perform(self.steps[6], ledger.submit_request, self.pool_handle, get_nym_txn_req6)

            # 7. Using the TrustAnchor create a Trustee (Trust Anchor should not be able to create Trustee) --------------------
            self.steps[7].set_name("Use TrustAnchor1 to create a Trustee")
            nym_txn_req7 = await perform(self.steps[7], ledger.build_nym_request, trustanchor1_did,
                                         trustee2_did, trustee2_verkey, None, Roles.TRUSTEE)
            await perform_with_expected_code(self.steps[7], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                                             trustanchor1_did, nym_txn_req7, expected_code=304)

            # 8. Verify GET_NYM for new Trustee--------------------------------------------------------------------------------
            self.steps[8].set_name("Verify get NYM for new trustee")
            get_nym_txn_req8 = await perform(self.steps[8], ledger.build_get_nym_request, trustanchor1_did, trustee2_did)
            await perform(self.steps[8], ledger.submit_request, self.pool_handle, get_nym_txn_req8)

            # 9. Verify that the TestTrustAnchorTrustee cannot create a new Steward
            self.steps[9].set_name("Verify a trustee cannot create a new Steward")
            nym_txn_req9 = await perform(self.steps[9], ledger.build_nym_request, trustee2_did, steward1_did,
                                         steward1_verkey, None, Roles.STEWARD)
            await perform_with_expected_code(self.steps[9], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                                             trustee2_did, nym_txn_req9, expected_code=304)

            # 10. Using the TrustAnchor blacklist a Trustee (TrustAnchor should not be able to blacklist Trustee)
            self.steps[10].set_name("Use TrustAnchor to blacklist a Trustee")
            nym_txn_req10 = await perform(self.steps[10], ledger.build_nym_request, trustanchor1_did, trustee1_did,
                                          trustee1_verkey, None, Roles.NONE)
            await perform_with_expected_code(self.steps[10], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                                             trustanchor1_did, nym_txn_req10, expected_code=304)

            # 11. Verify Trustee was not blacklisted by creating another Trustee------------------------------------------------
            self.steps[11].set_name("Verify Trustee was not blacklisted by creating another Trustee")
            nym_txn_req11 = await perform(self.steps[11], ledger.build_nym_request, trustee1_did, trustee2_did,
                                          trustee2_verkey, None, Roles.TRUSTEE)
            await perform(self.steps[11], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle, trustee1_did, nym_txn_req11)

            # 12. Using the TrustAnchor1 to create a Steward2 -----------------------------------------------------------------
            self.steps[12].set_name("TrustAnchor1 cannot create a Steward2")
            nym_txn_req12 = await perform(self.steps[12], ledger.build_nym_request, trustanchor1_did, steward2_did,
                                          steward2_verkey, None, Roles.STEWARD)
            await perform_with_expected_code(self.steps[12], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                                             trustanchor1_did, nym_txn_req12, expected_code=304)

            # 13. Using the Trustee1 create Steward1 -----------------------------------------------------------------
            self.steps[13].set_name("Using the Trustee1 create Steward1")
            nym_txn_req13 = await perform(self.steps[13], ledger.build_nym_request, trustee1_did, steward1_did,
                                          steward1_verkey, None, Roles.STEWARD)
            await perform(self.steps[13], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                          trustee1_did, nym_txn_req13)

            # 14. Now run the test to blacklist Steward1
            self.steps[14].set_name("Run the test to blacklist Steward1")
            nym_txn_req14 = await perform(self.steps[14], ledger.build_nym_request, trustanchor1_did, steward1_did,
                                          steward1_verkey, None, Roles.NONE)
            await perform_with_expected_code(self.steps[14], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                                             trustanchor1_did, nym_txn_req14, expected_code=304)

            # 15. Verify that a TrustAnchor1 cannot create another TrustAnchor3 -------------------------------------
            self.steps[15].set_name("Verify TrustAnchor1 cannot create a TrustAnchor3")
            nym_txn_req15 = await perform(self.steps[15], ledger.build_nym_request, trustanchor1_did, trustanchor3_did,
                                          trustanchor3_verkey, None, Roles.TRUST_ANCHOR)
            await perform_with_expected_code(self.steps[15], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                                             trustanchor1_did, nym_txn_req15, expected_code=304)

            # 16. Using the Trustee1 create TrustAnchor2 -----------------------------------------------------------------
            self.steps[16].set_name("Using the Trustee1 create Steward1")
            nym_txn_req16 = await perform(self.steps[16], ledger.build_nym_request, trustee1_did, trustanchor2_did,
                                          trustanchor2_verkey, None, Roles.TRUST_ANCHOR)
            await perform(self.steps[16], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                          trustee1_did, nym_txn_req16)

            # 17. Verify that a TrustAnchor1 cannot blacklist another TrustAnchor2 -------------------------------------
            self.steps[17].set_name("Verify TrustAnchor1 cannot blacklist TrustAnchor2")
            nym_txn_req17 = await perform(self.steps[17], ledger.build_nym_request, trustanchor1_did, trustanchor2_did,
                                          trustanchor2_verkey, None, Roles.NONE)
            await perform_with_expected_code(self.steps[17], ledger.sign_and_submit_request, self.pool_handle, self.wallet_handle,
                                             trustanchor1_did, nym_txn_req17, expected_code=304)

            for item in self.steps:
                item.to_string()
        except IndyError as e:
            print(Colors.FAIL + "Stop due to IndyError: " + str(e) + Colors.ENDC)
        except Exception as ex:
            print(Colors.FAIL + "Exception: " + str(ex) + Colors.ENDC)
        print("Test Scenario 11 -> completed")


if __name__ == '__main__':
    TestScenario11().execute_scenario()
