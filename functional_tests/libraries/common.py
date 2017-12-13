"""
Created on Nov 13, 2017

@author: khoi.ngo

Containing all functions that is common among test scenarios.
"""

import json
import os
import shutil
from indy import wallet, pool, ledger
from indy.error import IndyError
from .constant import Colors, Constant, Message
from . import utils


class Common:
    """
    Wrapper common function for test scenario.
    """

    @staticmethod
    async def prepare_pool_and_wallet(pool_name, wallet_name,
                                      pool_genesis_txn_file):
        """
        Prepare pool and wallet to use in a test case.

        :param pool_name: Name of the pool ledger configuration.
        :param wallet_name: Name of the wallet.
        :param pool_genesis_txn_file: path of pool_genesis_transaction file.
        :return: The pool handle and the wallet handle were created.
        """
        pool_handle = await \
            Common().create_and_open_pool(pool_name, pool_genesis_txn_file)

        wallet_handle = await \
            Common().create_and_open_wallet(pool_name, wallet_name)

        return pool_handle, wallet_handle

    @staticmethod
    async def clean_up_pool_and_wallet(pool_name, pool_handle,
                                       wallet_name, wallet_handle):
        """
        Clean up pool and wallet. Using as a post condition of a test case.

        :param pool_name: The name of the pool.
        :param pool_handle: The handle of the pool.
        :param wallet_name: The name of the wallet.
        :param wallet_handle: The handle of the wallet.
        """
        await Common.close_and_delete_wallet(wallet_name, wallet_handle)
        await Common.close_and_delete_pool(pool_name, pool_handle)

    @staticmethod
    def clean_up_pool_and_wallet_folder(pool_name, wallet_name):
        """
        Delete pool and wallet folder without using lib-indy.

        :param pool_name: The name of the pool.
        :param wallet_name: The name of the wallet.
        """
        Common.delete_pool_folder(pool_name)
        Common.delete_wallet_folder(wallet_name)

    @staticmethod
    async def build_and_send_nym_request(pool_handle, wallet_handle,
                                         submitter_did, target_did,
                                         target_verkey, alias, role):
        """
        Build a nym request and send it.

        :param pool_handle: pool handle returned by indy_open_pool_ledger.
        :param wallet_handle: wallet handle returned by indy_open_wallet.
        :param submitter_did: Id of Identity stored in secured Wallet.
        :param target_did: Id of Identity stored in secured Wallet.
        :param target_verkey: verification key.
        :param alias: alias.
        :param role: Role of a user NYM record.
        :raise Exception if the method has error.
        """
        nym_txn_req = await \
            ledger.build_nym_request(submitter_did, target_did,
                                     target_verkey, alias, role)
        await ledger.sign_and_submit_request(pool_handle, wallet_handle,
                                             submitter_did, nym_txn_req)

    @staticmethod
    async def create_and_open_pool(pool_name, pool_genesis_txn_file):
        """
        Creates a new local pool ledger configuration.
        Then open that pool and return the pool handle that can be used later
        to connect pool nodes.

        :param pool_name: Name of the pool ledger configuration.
        :param pool_genesis_txn_file: Pool configuration json. if NULL, then
        default config will be used.
        :return: The pool handle was created.
        """
        print(Colors.HEADER + "\nCreate Ledger\n" + Colors.ENDC)
        await Common.create_pool_ledger_config(pool_name,
                                               pool_genesis_txn_file)

        print(Colors.HEADER + "\nOpen pool ledger\n" + Colors.ENDC)
        pool_handle = await pool.open_pool_ledger(pool_name, None)
        return pool_handle

    @staticmethod
    async def create_and_open_wallet(pool_name, wallet_name):
        """
        Creates a new secure wallet with the given unique name.
        Then open that wallet and get the wallet handle that can
        be used later to use in methods that require wallet access.

        :param pool_name: Name of the pool that corresponds to this wallet.
        :param wallet_name: Name of the wallet.
        :return: The wallet handle was created.
        """
        print(Colors.HEADER + "\nCreate wallet\n" + Colors.ENDC)
        await wallet.create_wallet(pool_name, wallet_name, None, None, None)

        print(Colors.HEADER + "\nGet wallet handle\n" + Colors.ENDC)
        wallet_handle = await wallet.open_wallet(wallet_name, None, None)
        return wallet_handle

    @staticmethod
    async def close_pool_and_wallet(pool_handle, wallet_handle):
        """
        Close the pool and wallet with the pool and wallet handle.

        :param pool_handle: pool handle returned by indy_open_pool_ledger.
        :param wallet_handle: wallet handle returned by indy_open_wallet.
        :raise Exception if the method has error.
        """
        if pool_handle:
            print(Colors.HEADER + "\nClose pool\n" + Colors.ENDC)
            await pool.close_pool_ledger(pool_handle)

        if wallet_handle:
            print(Colors.HEADER + "\nClose wallet\n" + Colors.ENDC)
            await wallet.close_wallet(wallet_handle)

    @staticmethod
    async def delete_pool_and_wallet(pool_name, wallet_name):
        """
        Delete the pool and wallet with the pool and wallet name.

        :param pool_name: Name of the pool that corresponds to this wallet.
        :param wallet_name: Name of the wallet to delete.
        :raise Exception if the method has error.
        """
        if pool_name:
            print(Colors.HEADER + "\nDelete pool\n" + Colors.ENDC)
            await pool.delete_pool_ledger_config(pool_name)

        if wallet_name:
            print(Colors.HEADER + "\nDelete wallet\n" + Colors.ENDC)
            await wallet.delete_wallet(wallet_name, None)

    @staticmethod
    async def create_and_open_pool_ledger_for_steps(steps, pool_name,
                                                    pool_genesis_txn_file,
                                                    pool_config=None):
        # Create a pool ledger config.
        steps.add_step("Create pool ledger config")
        await utils.perform(steps, Common.create_pool_ledger_config, pool_name,
                            pool_genesis_txn_file, ignore_exception=False)

        # Open pool ledger.
        steps.add_step("Open pool ledger")
        result = await utils.perform(steps, pool.open_pool_ledger, pool_name,
                                     pool_config, ignore_exception=False)

        return result

    @staticmethod
    async def create_and_open_wallet_for_steps(steps, wallet_name, pool_name,
                                               wallet_config=None, xtype=None,
                                               credentials=None,
                                               runtime_config=None):
        # Create a wallet.
        steps.add_step("Create wallet")
        await utils.perform(steps, wallet.create_wallet, pool_name,
                            wallet_name, xtype, wallet_config, credentials)

        # Open wallet.
        steps.add_step("Open wallet")
        result = await utils.perform(steps, wallet.open_wallet, wallet_name,
                                     runtime_config, credentials)

        return result

    @staticmethod
    async def create_pool_ledger_config(pool_name, pool_genesis_txn_file):
        if os.path.exists(pool_genesis_txn_file) is not True:
            error_message = (Colors.FAIL +
                             "\n{}\n".format(Message.ERR_PATH_DOES_NOT_EXIST.
                                             format(pool_genesis_txn_file)) +
                             Colors.ENDC)
            raise ValueError(error_message)

        pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_file)})
        await pool.create_pool_ledger_config(pool_name, pool_config)

    @staticmethod
    async def close_and_delete_pool(pool_name, pool_handle):
        if pool_handle:
            try:
                utils.print_header("\nClose pool\n")
                await pool.close_pool_ledger(pool_handle)
            except IndyError as ie:
                utils.print_error(str(ie))

        if pool_name:
            try:
                utils.print_header("\nDelete pool\n")
                await pool.delete_pool_ledger_config(pool_name)
            except IndyError as ie:
                utils.print_error(str(ie))

    @staticmethod
    async def close_and_delete_wallet(wallet_name, wallet_handle,
                                      credentials=None):
        if wallet_handle:
            try:
                utils.print_header("\nClose wallet\n")
                await wallet.close_wallet(wallet_handle)
            except IndyError as ie:
                utils.print_error(str(ie))

        if wallet_name:
            try:
                utils.print_header("\nDelete wallet\n")
                await wallet.delete_wallet(wallet_name, credentials)
            except IndyError as ie:
                utils.print_error(str(ie))

    @staticmethod
    def delete_pool_folder(pool_name: str):
        if not pool_name:
            return

        work_dir = Constant.work_dir
        utils.print_header("\nClean up pool ledger\n")
        if os.path.exists(work_dir + "/pool/" + pool_name):
            try:
                shutil.rmtree(work_dir + "/pool/" + pool_name)
            except IOError as E:
                print(Colors.FAIL + str(E) + Colors.ENDC)

    @staticmethod
    def delete_wallet_folder(wallet_name: str):
        if not wallet_name:
            return

        utils.print_header("\nClean up wallet\n")
        work_dir = Constant.work_dir
        if os.path.exists(work_dir + "/wallet/" + wallet_name):
            try:
                shutil.rmtree(work_dir + "/wallet/" + wallet_name)
            except IOError as E:
                print(Colors.FAIL + str(E) + Colors.ENDC)
