"""
Created on Jan 8, 2018

@author: nhan.nguyen
"""
import json

from indy import anoncreds, signus
from utilities import utils, common, constant
from test_scripts.functional_tests.anoncreds import anoncreds_test_base
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestProverGetClaimByFilteringWithSchemaNo(AnoncredsTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)
        # 3. Create 'issuer1_did'.
        self.steps.add_step("Create 'issuer1_did'")
        (issuer1_did, _) = await utils.perform(self.steps,
                                               signus.create_and_store_my_did,
                                               self.wallet_handle, "{}")

        # 4. Create 'issuer2_did'.
        self.steps.add_step("Create 'issuer2_did'")
        (issuer2_did, _) = await utils.perform(self.steps,
                                               signus.create_and_store_my_did,
                                               self.wallet_handle, "{}")

        # 5. Create 'prover_did'.
        self.steps.add_step("Create 'prover_did'")
        (prover_did, _) = await utils.perform(self.steps,
                                              signus.create_and_store_my_did,
                                              self.wallet_handle, '{}')

        # 6. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 7. Create and store claim definition with 'issuer1_did'.
        self.steps.add_step("Create and store claim definition "
                            "with 'issuer1_did'")
        gvt_claim_def = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer1_did,
                          json.dumps(constant.gvt_schema),
                          constant.signature_type, False)

        # 8. Create and store other claim definition with 'issuer2_did'.
        self.steps.add_step("Create and store other claim definition "
                            "with 'issuer2_did'")
        xyz_claim_def = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer2_did,
                          json.dumps(constant.xyz_schema),
                          constant.signature_type, False)

        # 9. Create claim request with 'issuer1_did'.
        self.steps.add_step("Create claim request with 'issuer1_did'")
        claim_offer = utils.create_claim_offer(issuer1_did,
                                               constant.gvt_schema_seq)
        gvt_claim_req = await \
            utils.perform(self.steps,
                          anoncreds.prover_create_and_store_claim_req,
                          self.wallet_handle, prover_did,
                          json.dumps(claim_offer), gvt_claim_def,
                          constant.secret_name)

        # 10. Create claim.
        self.steps.add_step("Create claim")
        (_, created_gvt_claim) = await \
            utils.perform(self.steps, anoncreds.issuer_create_claim,
                          self.wallet_handle, gvt_claim_req,
                          json.dumps(constant.gvt_claim), -1)

        # 11. Store claim into wallet.
        self.steps.add_step("Store claim into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_gvt_claim)

        # 12. Create other claim request with 'issuer2_did'.
        self.steps.add_step("Create other claim request with 'issuer2_did'")
        claim_offer = utils.create_claim_offer(issuer2_did,
                                               constant.xyz_schema_seq)
        xyz_claim_req = await \
            utils.perform(self.steps,
                          anoncreds.prover_create_and_store_claim_req,
                          self.wallet_handle, prover_did,
                          json.dumps(claim_offer), xyz_claim_def,
                          constant.secret_name)

        # 13. Create other claim.
        self.steps.add_step("Create claim")
        (_, created_xyz_claim) = await \
            utils.perform(self.steps, anoncreds.issuer_create_claim,
                          self.wallet_handle, xyz_claim_req,
                          json.dumps(constant.xyz_claim), -1)

        # 14. Store claim into wallet.
        self.steps.add_step("Store claim into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_xyz_claim)

        # 15. Get stored claims by filtering with gvt_schema_no.
        self.steps.add_step("Get stored claims by "
                            "filtering with gvt_schema_no")
        filter_json = json.dumps({"schema_seq_no": constant.gvt_schema_seq})
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_claims,
                                         self.wallet_handle, filter_json)

        lst_claims = json.loads(lst_claims)

        # 16. Check returned list claims.
        self.steps.add_step("Check returned list claims")
        err_msg = "Cannot get claims from wallet"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: len(lst_claims) == 1)

        # 17. Check lst_claims[0]['claim_uuid'].
        # 18. Check lst_claims[0]['attrs'].
        # 19. Check lst_claims[0]['issuer_did'].
        # 20. Check lst_claims[0]['schema_seq_no'].
        anoncreds_test_base.check_gotten_claim_is_valid(
            self.steps, lst_claims[0], constant.gvt_claim,
            issuer1_did, constant.gvt_schema_seq)


if __name__ == '__main__':
    TestProverGetClaimByFilteringWithSchemaNo().execute_scenario()
