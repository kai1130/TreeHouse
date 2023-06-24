import retrieve as r 

from hedera import (
    Hbar,
    ContractCallQuery,
    ContractId
    )
from get_client import client, OPERATOR_KEY

def read_catalog(catalog):

    catalog_dict = {}

    for idx, row in catalog.iterrows():

        print(f'Retrieving Data for {row["name"]}')

        contract_id = ContractId.fromString(row['contract_id'])

        query_result = r.read_hedera_contract(contract_id)

        result_dict = getattr(r, row['callable'])(query_result)

        result_dict = r.clean_dict(result_dict)

        if row['category'] not in catalog_dict:
            catalog_dict[row['category']] = {}

        catalog_dict[row['category']][row['name']] = result_dict

    return catalog_dict
