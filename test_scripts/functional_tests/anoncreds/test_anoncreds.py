import json, logging
from indy import anoncreds, signus
from utilities import utils, common, constant
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class ReproduceIssue(AnoncredsTestBase):
    async def execute_test_steps(self):
        logging.basicConfig(level=logging.DEBUG)
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create 'issuer_did'.x
        self.steps.add_step("Create 'issuer_did'")
        (issuer_did, _) = await utils.perform(self.steps,
                                              signus.create_and_store_my_did,
                                              self.wallet_handle, "{}")

        # 4. Create and store claim definition and store
        # returned result as 'claim_def'.
        self.steps.add_step("Create and store claim definition and "
                            "store returned result as 'claim_def'")
        claim_def = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer_did,
                          json.dumps(constant.gvt_schema),
                          constant.signature_type, True)

        claim_def_primary = json.loads(claim_def)['data']['primary']

        # 5. Create revocation registry.
        self.steps.add_step("Create revocation registry")
        revocation_json = await anoncreds.issuer_create_and_store_revoc_reg(
            self.wallet_handle, issuer_did, constant.gvt_schema_seq, 1)
        print(revocation_json)


if __name__ == '__main__':
    ReproduceIssue().execute_scenario()