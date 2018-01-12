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


class TestProverGetClaimByFilteringWithSchemaNoAndIssuerDid(AnoncredsTestBase):
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

        # 7. Create and store claim definition
        # with 'issuer1_did' and 'gvt_schema'.
        self.steps.add_step("Create and store claim definition "
                            "with 'issuer1_did' and 'gvt_schema'")
        gvt_claim_def1 = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer1_did,
                          json.dumps(constant.gvt_schema),
                          constant.signature_type, False)

        # 8. Create and store other claim definition
        # with 'issuer2_did' with 'xyz_schema'.
        self.steps.add_step("Create and store other claim definition "
                            "with 'issuer2_did' with 'xyz_schema'")
        xyz_claim_def = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer2_did,
                          json.dumps(constant.xyz_schema),
                          constant.signature_type, False)

        # 9. Create and store other claim definition
        # with 'issuer2_did' and 'gvt_schema'.
        self.steps.add_step("Create and store other claim definition "
                            "with 'issuer2_did' and 'gvt_schema'")
        gvt_claim_def2 = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer2_did,
                          json.dumps(constant.gvt_schema),
                          constant.signature_type, False)

        # 10. Create claim request with 'issuer1_did' and 'gvt_schema'.
        self.steps.add_step("Create claim request with "
                            "'issuer1_did' and 'gvt_schema'")
        claim_offer = utils.create_claim_offer(issuer1_did,
                                               constant.gvt_schema_seq)
        gvt_claim_req1 = await \
            utils.perform(self.steps,
                          anoncreds.prover_create_and_store_claim_req,
                          self.wallet_handle, prover_did,
                          json.dumps(claim_offer), gvt_claim_def1,
                          constant.secret_name)

        # 11. Create claim with 'gvt_schema'.
        self.steps.add_step("Create claim with 'gvt_schema'")
        (_, created_gvt_claim1) = await \
            utils.perform(self.steps, anoncreds.issuer_create_claim,
                          self.wallet_handle, gvt_claim_req1,
                          json.dumps(constant.gvt_claim), -1)

        # 12. Store created claim into wallet.
        self.steps.add_step("Store created claim into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_gvt_claim1)

        # 13. Create other claim request with 'issuer2_did' and 'xyz_schema'.
        self.steps.add_step("Create other claim request with "
                            "'issuer2_did' and 'xyz_schema'")
        claim_offer = utils.create_claim_offer(issuer2_did,
                                               constant.xyz_schema_seq)
        xyz_claim_req = await \
            utils.perform(self.steps,
                          anoncreds.prover_create_and_store_claim_req,
                          self.wallet_handle, prover_did,
                          json.dumps(claim_offer), xyz_claim_def,
                          constant.secret_name)

        # 14. Create other claim with 'xyz_schema'.
        self.steps.add_step("Create other claim with 'xyz_schema'")
        (_, created_xyz_claim) = await \
            utils.perform(self.steps, anoncreds.issuer_create_claim,
                          self.wallet_handle, xyz_claim_req,
                          json.dumps(constant.xyz_claim), -1)

        # 15. Store created claim into wallet.
        self.steps.add_step("Store created claim into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_xyz_claim)

        # 16. Create another claim request with 'issuer2_did' and 'gvt_schema'.
        self.steps.add_step("Create another claim request with "
                            "'issuer2_did' and 'gvt_schema'")
        claim_offer = utils.create_claim_offer(issuer2_did,
                                               constant.gvt_schema_seq)
        gvt_claim_req2 = await \
            utils.perform(self.steps,
                          anoncreds.prover_create_and_store_claim_req,
                          self.wallet_handle, prover_did,
                          json.dumps(claim_offer), gvt_claim_def2,
                          constant.secret_name)

        # 17. Create claim with 'gvt_schema'.
        self.steps.add_step("Create claim with 'gvt_schema'")
        (_, created_gvt_claim2) = await \
            utils.perform(self.steps, anoncreds.issuer_create_claim,
                          self.wallet_handle, gvt_claim_req2,
                          json.dumps(constant.gvt_other_claim), -1)

        # 18. Store created claim into wallet.
        self.steps.add_step("Store created claim into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_gvt_claim2)

        # 19. Get claims by proof req.
        self.steps.add_step("Get claims by proof request")
        proof_req = json.dumps(
            {'nonce': '1', 'name': 'proof_req_1', 'version': '0.1',
             'requested_attrs': {'attr1_referent': {'name': 'name'}},
             'requested_predicates': {
                 'predicate1_referent': {'attr_name': 'age', 'p_type': 'GE',
                                         'value': 25}}})
        temp = await utils.perform(self.steps,
                                   anoncreds.prover_get_claims_for_proof_req,
                                   self.wallet_handle, proof_req)


if __name__ == '__main__':
    TestProverGetClaimByFilteringWithSchemaNoAndIssuerDid().execute_scenario()
