import os
import base64

from algosdk.v2client import algod, indexer
from algosdk import mnemonic, account
from algosdk.future import transaction

ALGOD_ENDPOINT = os.environ['ALGOD_ENDPOINT']
ALGOD_TOKEN = os.environ['ALGOD_TOKEN']
INDEXER_ENDPOINT = os.environ['INDEXER_ENDPOINT']
INDEXER_TOKEN = os.environ['INDEXER_TOKEN']
TEST_ACCOUNT_PRIVATE_KEY = mnemonic.to_private_key(os.environ['TEST_ACCOUNT_PRIVATE_KEY'])
TEST_ACCOUNT_ADDRESS = account.address_from_private_key(TEST_ACCOUNT_PRIVATE_KEY)

ESCROW_LOGICSIG = os.environ['ESCROW_LOGICSIG']
ESCROW_ADDRESS = os.environ['ESCROW_ADDRESS']

VALIDATOR_INDEX = int(os.environ['VALIDATOR_INDEX'])
MANAGER_INDEX = int(os.environ['MANAGER_INDEX'])
TOKEN1_INDEX = int(os.environ['TOKEN1_INDEX'])
TOKEN2_INDEX = int(os.environ['TOKEN2_INDEX'])
LIQUIDITY_TOKEN_INDEX = int(os.environ['LIQUIDITY_TOKEN_INDEX'])

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ENDPOINT, headers={
    "x-api-key": ALGOD_TOKEN
})
indexer_client = indexer.IndexerClient(INDEXER_TOKEN, INDEXER_ENDPOINT, headers={
    "x-api-key": INDEXER_TOKEN
})

def wait_for_transaction(transaction_id):
    suggested_params = algod_client.suggested_params()
    algod_client.status_after_block(suggested_params.first + 2)
    result = indexer_client.search_transactions(txid=transaction_id)
    assert len(result['transactions']) == 1, result
    return result['transactions'][0]

def withdraw_liquidity():
    print("Building withdraw liquidity atomic transaction group...")

    encoded_app_args = [
        bytes("w", "utf-8"),
        bytes("5", "utf-8"),
        bytes("5", "utf-8"),
    ]

    # Transaction to Validator
    txn_1 = transaction.ApplicationCallTxn(
        sender=TEST_ACCOUNT_ADDRESS,
        sp=algod_client.suggested_params(),
        index=VALIDATOR_INDEX,
        on_complete=transaction.OnComplete.NoOpOC,
        accounts=[ESCROW_ADDRESS, ESCROW_ADDRESS],
        app_args=encoded_app_args,
        foreign_assets=[LIQUIDITY_TOKEN_INDEX]
    )

    # Transaction to Manager
    txn_2 = transaction.ApplicationCallTxn(
        sender=TEST_ACCOUNT_ADDRESS,
        sp=algod_client.suggested_params(),
        index=MANAGER_INDEX,
        on_complete=transaction.OnComplete.NoOpOC,
        accounts=[ESCROW_ADDRESS, ESCROW_ADDRESS],
        app_args=encoded_app_args,
        foreign_assets=[LIQUIDITY_TOKEN_INDEX]
    )

    # Transaction to Escrow
    txn_3 = transaction.AssetTransferTxn(
        sender=TEST_ACCOUNT_ADDRESS,
        sp=algod_client.suggested_params(),
        receiver=ESCROW_ADDRESS,
        amt=10,
        index=LIQUIDITY_TOKEN_INDEX
    )

    # Get group ID and assign to transactions
    gid = transaction.calculate_group_id([txn_1, txn_2, txn_3])
    txn_1.group = gid
    txn_2.group = gid
    txn_3.group = gid

    # Sign transactions
    stxn_1 = txn_1.sign(TEST_ACCOUNT_PRIVATE_KEY)
    stxn_2 = txn_2.sign(TEST_ACCOUNT_PRIVATE_KEY)
    stxn_3 = txn_3.sign(TEST_ACCOUNT_PRIVATE_KEY)

    # Broadcast the transactions
    signed_txns = [stxn_1, stxn_2, stxn_3]
    tx_id = algod_client.send_transactions(signed_txns)

    # Wait for transaction
    wait_for_transaction(tx_id)

    print(f"Withdraw liquidity transaction sent from User to AlgoSwap successfully! Tx ID: https://testnet.algoexplorer.io/tx/{tx_id}")

    print()

def get_token1_refund():
    print("Attempting to get refund of Token 1 from Escrow...")

    encoded_app_args = [
        bytes("r", "utf-8")
    ]

    # Transaction to Validator
    txn_1 = transaction.ApplicationCallTxn(
        sender=TEST_ACCOUNT_ADDRESS,
        sp=algod_client.suggested_params(),
        index=VALIDATOR_INDEX,
        on_complete=transaction.OnComplete.NoOpOC,
        accounts=[ESCROW_ADDRESS],
        app_args=encoded_app_args
    )

    # Transaction to Manager
    txn_2 = transaction.ApplicationCallTxn(
        sender=TEST_ACCOUNT_ADDRESS,
        sp=algod_client.suggested_params(),
        index=MANAGER_INDEX,
        on_complete=transaction.OnComplete.NoOpOC,
        accounts=[ESCROW_ADDRESS],
        app_args=encoded_app_args
    )

    # Calculate unused_token1
    unused_token1 = 0
    results = algod_client.account_info(TEST_ACCOUNT_ADDRESS)
    local_state = results['apps-local-state'][0]
    for index in local_state:
        if local_state[index] == MANAGER_INDEX:
            unused_token1 = local_state['U1']
    
    print(f"User unused Token 1 is {unused_token1}")

    # Transaction to get refund from Escrow
    program = base64.b64decode(ESCROW_LOGICSIG)
    lsig = transaction.LogicSig(program)

    txn_3 = transaction.AssetTransferTxn(
        sender=ESCROW_ADDRESS,
        sp=algod_client.suggested_params(),
        receiver=TEST_ACCOUNT_ADDRESS,
        amt=unused_token1,
        index=TOKEN1_INDEX
    )

    # Get group ID and assign to transactions
    gid = transaction.calculate_group_id([txn_1, txn_2, txn_3])
    txn_1.group = gid
    txn_2.group = gid
    txn_3.group = gid

    # Sign transactions
    stxn_1 = txn_1.sign(TEST_ACCOUNT_PRIVATE_KEY)
    stxn_2 = txn_2.sign(TEST_ACCOUNT_PRIVATE_KEY)
    stxn_3 = txn_3.sign(TEST_ACCOUNT_PRIVATE_KEY)

    # Broadcast the transactions
    signed_txns = [stxn_1, stxn_2, stxn_3]
    tx_id = algod_client.send_transactions(signed_txns)

    # Wait for transaction
    wait_for_transaction(tx_id)

    print(f"Got refund of Token 1 from AlgoSwap to User successfully! Tx ID: https://testnet.algoexplorer.io/tx/{tx_id}")

    print()

def get_token2_refund():
    pass

if __name__ == "__main__":
    withdraw_liquidity()
    get_token1_refund()
    get_token2_refund()