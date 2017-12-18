"""
Created on Dec 15, 2017

@author: nhan.nguyen
"""

import json
from indy import anoncreds, signus
from libraries import utils, common, constant
from test_scripts.functional_tests.anoncreds.anoncreds_test_base \
    import AnoncredsTestBase


class TestIssuerCreateAndStoreClaimDefWithValidData(AnoncredsTestBase):
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

        # 4. Create and store claim definition and store
        # returned result as 'claim_def'.
        self.steps.add_step("Create and store claim definition and "
                            "store returned result as 'claim_def'")
        claim_def = await \
            utils.perform(self.steps,
                          anoncreds.issuer_create_and_store_claim_def,
                          self.wallet_handle, issuer_did,
                          json.dumps(constant.sample_schema1),
                          constant.signature_type, False)

        claim_def_primary = json.loads(claim_def)['data']['primary']

        # 5. Check len(claim_def['data']['primary']['r']).
        self.steps.add_step("Check len(claim_def['data']['primary']['r'])")
        error_message = "Length of claim_def['data']['primary']['r'] " \
                        "is not equal with 4"
        utils.check(self.steps, error_message,
                    condition=lambda: len(claim_def_primary['r']) == 4)

        # 6. Check claim_def['data']['primary']['n'].
        self.steps.add_step("Check claim_def['data']['primary']['n']")
        error_message = "Length of claim_def['data']['primary']['n'] " \
                        "is a not empty list"
        utils.check(self.steps, error_message,
                    condition=lambda: isinstance(claim_def_primary['n'], list)
                    and len(claim_def_primary['n']) > 0)

        # 7. Check claim_def['data']['primary']['s'].
        self.steps.add_step("Check claim_def['data']['primary']['s']")
        error_message = "Length of claim_def['data']['primary']['s'] " \
                        "is a not empty list"
        utils.check(self.steps, error_message,
                    condition=lambda: isinstance(claim_def_primary['s'], list)
                    and len(claim_def_primary['s']) > 0)

        # 8. Check claim_def['data']['primary']['rms'].
        self.steps.add_step("Check claim_def['data']['primary']['rms']")
        error_message = "Length of claim_def['data']['primary']['rms'] " \
                        "is a not empty list"
        utils.check(self.steps, error_message,
                    condition=lambda:
                    isinstance(claim_def_primary['rms'], list)
                    and len(claim_def_primary['rms']) > 0)
        # 9. Check claim_def['data']['primary']['z'].
        self.steps.add_step("Check claim_def['data']['primary']['z']")
        error_message = "Length of claim_def['data']['primary']['z'] " \
                        "is a not empty list"
        utils.check(self.steps, error_message,
                    condition=lambda: isinstance(claim_def_primary['z'], list)
                    and len(claim_def_primary['z']) > 0)

        # 10. Check claim_def['data']['primary']['rctxt'].
        self.steps.add_step("Check claim_def['data']['primary']['rctxt']")
        error_message = "Length of claim_def['data']['primary']['rctxt'] " \
                        "is a not empty list"
        utils.check(self.steps, error_message,
                    condition=lambda:
                    isinstance(claim_def_primary['rctxt'], list)
                    and len(claim_def_primary['rctxt']) > 0)


if __name__ == '__main__':
    TestIssuerCreateAndStoreClaimDefWithValidData().execute_scenario()
