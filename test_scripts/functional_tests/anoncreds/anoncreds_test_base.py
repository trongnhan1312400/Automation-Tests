"""
Created on Dec 15, 2017

@author: nhan.nguyen

Containing a base class for anoncreds testing.
"""

from utilities import common, utils
from utilities.test_scenario_base import TestScenarioBase


class AnoncredsTestBase(TestScenarioBase):
    def __init__(self):
        if self.__class__ is not AnoncredsTestBase:
            super().__init__()

    async def execute_precondition_steps(self):
        common.delete_wallet_folder(self.wallet_name)

    async def execute_postcondition_steps(self):
        await common.close_and_delete_wallet(self.wallet_name,
                                             self.wallet_handle)

    def execute_scenario(self, time_out=None):
        if self.__class__ is not AnoncredsTestBase:
            super().execute_scenario(time_out)


def check_claim_attrs(claim_attrs, expected_claim):
    for key in expected_claim.keys():
        if claim_attrs[key] != expected_claim[key][0]:
            return False
    return True


def check_gotten_claim_is_valid(steps, gotten_claim, expected_claim_json,
                                issuer_did, schema_no):
    # Check lst_claims[0]['claim_uuid'].
    steps.add_step("Check lst_claims[0]['claim_uuid']")
    err_msg = "Claim's uuid is empty"
    utils.check(steps, error_message=err_msg,
                condition=lambda: len(gotten_claim["claim_uuid"]) > 0)

    # Check lst_claims[0]['attrs'].
    steps.add_step("Check lst_claims[0]['attrs']")
    claim_attrs = gotten_claim["attrs"]
    err_msg = "lst_claims[0]['attrs'] mismatches"
    utils.check(steps, error_message=err_msg,
                condition=lambda: check_claim_attrs(claim_attrs,
                                                    expected_claim_json))

    # Check lst_claims[0]['issuer_did'].
    steps.add_step("Check lst_claims[0]['issuer_did']")
    err_msg = "Issuer's did mismatches"
    utils.check(steps, error_message=err_msg,
                condition=lambda: gotten_claim["issuer_did"] == issuer_did)

    # 14. Check lst_claims[0]['issuer_did'].
    steps.add_step("Check lst_claims[0]['issuer_did']")
    err_msg = "Issuer's did mismatches"
    utils.check(steps, error_message=err_msg,
                condition=lambda: gotten_claim["schema_seq_no"] ==
                schema_no)
