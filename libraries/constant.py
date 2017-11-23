"""
Created on Nov 9, 2017

@author: khoi.ngo

Contains all constant that is necessary to execute test scenario.
"""


class Colors:
    """
    Class to set the colors for text.
    Syntax:  print(Colors.OKGREEN +"TEXT HERE" +Colors.ENDC)
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # Normal default color.
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Roles:
    """
    Class to define roles.
    """
    TRUSTEE = "TRUSTEE"
    STEWARD = "STEWARD"
    TRUST_ANCHOR = "TRUST_ANCHOR"
    TGB = "TGB"  # obsolete.
    NONE = ""


class Constant:
    """
    Class Constant store some necessary paths.
    """
    import os
    user_home = os.path.expanduser('~') + os.sep
    work_dir = user_home + ".indy"
    seed_default_trustee = "000000000000000000000000Trustee1"
    pool_genesis_txn_file = "/var/lib/indy/sandbox/pool_transactions_sandbox_genesis"
    domain_transactions_sandbox_genesis = "/var/lib/indy/sandbox/domain_transactions_sandbox_genesis"
    original_pool_genesis_txn_file = "/var/lib/indy/sandbox/original_pool_transactions_sandbox_genesis"
