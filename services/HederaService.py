import os 
from credentials import OPERATOR_ID, OPERATOR_KEY

os.environ['OPERATOR_ID'] = OPERATOR_ID
os.environ['OPERATOR_KEY'] = OPERATOR_KEY

import pandas as pd

from hedera import (
    Hbar,
    FileCreateTransaction,
    ContractCreateTransaction
    )
from get_client import client, OPERATOR_KEY

def jsons_to_df(catalog):

    catalog_df = pd.DataFrame(catalog)
    catalog_df['contract_id'] = None
    
    return catalog_df

def get_bin_contents(path):
    
    with open(path, encoding='UTF8') as f:
        contents = f.read()
    
    return contents

def create_hedera_contract(path):
    
    contents = get_bin_contents(path)

    txn = (
        FileCreateTransaction()
        .setKeys(OPERATOR_KEY)
        .setContents(contents)
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

def deploy_catalog(catalog):

    catalog_df = jsons_to_df(catalog)
    
    for idx, row in catalog_df.iterrows():
        
        print(f'Deploying {row["name"]} to Hedera')

        row['contract_id'] = create_hedera_contract(row['binpath'])
        
        print('')

    return catalog_df