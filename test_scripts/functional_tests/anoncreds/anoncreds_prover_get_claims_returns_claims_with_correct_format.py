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


class TestProverGetClaimReturnCorrectFormat(AnoncredsTestBase):
    async def execute_test_steps(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)
        # 3. Create 'issuer_did'.
        self.steps.add_step("Create 'issuer_did'")
        (issuer_did, _) = await utils.perform(self.steps,
                                              signus.create_and_store_my_did,
                                              self.wallet_handle, "{}")

        # 4. Create 'prover_did'.
        self.steps.add_step("Create 'prover_did'")
        (prover_did, _) = await utils.perform(self.steps,
                                              signus.create_and_store_my_did,
                                              self.wallet_handle, '{}')

        # 5. Create master secret.
        self.steps.add_step("Create master secret")
        await utils.perform(self.steps, anoncreds.prover_create_master_secret,
                            self.wallet_handle, constant.secret_name)

        # 6. Create and store claim definition.
        self.steps.add_step("Create and store claim definition")
        claim_def = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer_did,
                          json.dumps(constant.gvt_schema),
                          constant.signature_type, False)

        # 7. Create claim request.
        self.steps.add_step("Create claim request")
        claim_offer = utils.create_claim_offer(issuer_did,
                                               constant.gvt_schema_seq)
        claim_req = await \
            utils.perform(self.steps,
                          anoncreds.prover_create_and_store_claim_req,
                          self.wallet_handle, prover_did,
                          json.dumps(claim_offer), claim_def,
                          constant.secret_name)

        # 8. Create claim.
        self.steps.add_step("Create claim")
        (_, created_claim) = await \
            utils.perform(self.steps, anoncreds.issuer_create_claim,
                          self.wallet_handle, claim_req,
                          json.dumps(constant.gvt_claim), -1)

        # 9. Store claim into wallet.
        self.steps.add_step("Store claim into wallet")
        await utils.perform(self.steps, anoncreds.prover_store_claim,
                            self.wallet_handle, created_claim)

        # 10. Get claims store in wallet.
        self.steps.add_step("Get claims store in wallet")
        lst_claims = await utils.perform(self.steps,
                                         anoncreds.prover_get_claims,
                                         self.wallet_handle, "{}")

        lst_claims = json.loads(lst_claims)

        # 11. Check returned claims.
        self.steps.add_step("Check returned claims")
        err_msg = "Returned claims is not a list"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: isinstance(lst_claims, list))

        # 12. Check lst_claims[0].
        self.steps.add_step("Check lst_claims[0]")
        err_msg = "Length of lst_claim[0] is incorrect"
        utils.check(self.steps, error_message=err_msg,
                    condition=lambda: len(lst_claims[0]))

        # 13. Check lst_claims[0]['claim_uuid'].
        # 14. Check lst_claims[0]['attrs'].
        # 15. Check lst_claims[0]['issuer_did'].
        # 16. Check lst_claims[0]['schema_seq_no'].
        anoncreds_test_base.check_gotten_claim_is_valid(
            self.steps, lst_claims[0], constant.gvt_claim,
            issuer_did, constant.gvt_schema_seq)


if __name__ == '__main__':
    TestProverGetClaimReturnCorrectFormat().execute_scenario()
