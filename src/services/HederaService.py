import os 
from credentials import OPERATOR_ID, OPERATOR_KEY

from hedera import (
    Hbar,
    FileCreateTransaction,
    ContractCreateTransaction
    )

print(os.environ)    

def createClient():
    pass


def create_hedera_contract(bin_str, operator_key):

    txn = (
        FileCreateTransaction()
        .setKeys(OPERATOR_KEY)
        .setContents(bin_str)
        .setMaxTransactionFee(Hbar(100))
        .execute(client))

    receipt = txn.getReceipt(client)
    fileId = receipt.fileId

    print(f" - Contract Bytecode File: {fileId.toString()}")

    txn = (
        ContractCreateTransaction()
        .setGas(1000000)
        .setBytecodeFileId(fileId)
        .setAdminKey(OPERATOR_KEY)
        .execute(client))

    receipt = txn.getReceipt(client)
    contractId = receipt.contractId

    print(f" - Contract ID: {contractId.toString()}")
    
    return contractId.toString()
