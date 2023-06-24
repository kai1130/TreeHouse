import os
import googlemaps
from datetime import datetime
from credentials import gmaps_api, OPERATOR_ID, OPERATOR_KEY

gmaps = googlemaps.Client(key=gmaps_api)
os.environ['OPERATOR_ID'] = OPERATOR_ID
os.environ['OPERATOR_KEY'] = OPERATOR_KEY

from hedera import (
    Hbar,
    ContractCallQuery,
    )

from get_client import client, OPERATOR_KEY

def read_hedera_contract(contractId):

    query_result = (
        ContractCallQuery()
        .setGas(300000)
        .setContractId(contractId)
        .setFunction("attr")
        .setQueryPayment(Hbar(100))
        .execute(client))
    
    return query_result

def retrieve_black_seat_dict(query_result):
    attribute_dict = {}
    
    attribute_dict['name'] = query_result.getString(0)
    attribute_dict['price'] = query_result.getInt64(1)
    attribute_dict['manufacturer'] = query_result.getString(2)
    attribute_dict['addr'] = query_result.getString(3)
    attribute_dict['weight'] = query_result.getInt64(4)
    attribute_dict['materials_leather'] = query_result.getInt64(5)
    attribute_dict['materials_metal'] = query_result.getInt64(6)
    
    return attribute_dict

def retrieve_white_seat_dict(query_result):
    attribute_dict = {}
    
    attribute_dict['name'] = query_result.getString(0)
    attribute_dict['price'] = query_result.getInt64(1)
    attribute_dict['manufacturer'] = query_result.getString(2)
    attribute_dict['addr'] = query_result.getString(3)
    attribute_dict['weight'] = query_result.getInt64(4)
    attribute_dict['materials_leatherette'] = query_result.getInt64(5)
    attribute_dict['materials_metal'] = query_result.getInt64(6)
    
    return attribute_dict

def retrieve_wheel_dict(query_result):
    
    attribute_dict = {}
    
    attribute_dict['name'] = query_result.getString(0)
    attribute_dict['price'] = query_result.getInt64(1)
    attribute_dict['manufacturer'] = query_result.getString(2)
    attribute_dict['addr'] = query_result.getString(3)
    attribute_dict['weight'] = query_result.getInt64(4)
    attribute_dict['materials_rubber'] = query_result.getInt64(5)
    attribute_dict['materials_metal'] = query_result.getInt64(6)
    
    return attribute_dict

def retrieve_model_dict(query_result):
    attribute_dict = {}
    
    attribute_dict['name'] = query_result.getString(0)
    attribute_dict['price'] = query_result.getInt64(1)
    attribute_dict['manufacturer'] = query_result.getString(2)
    attribute_dict['addr'] = query_result.getString(3)
    attribute_dict['weight'] = query_result.getInt64(4)
    attribute_dict['materials_metal'] = query_result.getInt64(5)
    attribute_dict['materials_plastic'] = query_result.getInt64(6)
    attribute_dict['options_seats'] = query_result.getString(7)
    attribute_dict['options_wheels'] = query_result.getString(8)
    
    return attribute_dict

def clean_dict(result_dict):
    
    result_dict['materials'] = {}
    result_dict['options'] = {}

    for k in list(result_dict.keys()):
        if k.startswith('materials') and '_' in k:
            _, mat = k.split('_')
            result_dict['materials'][mat] = result_dict[k]
        if k.startswith('options') and '_' in k:
            _, opt = k.split('_')
            result_dict['options'][opt] = None if result_dict[k] == '' else result_dict[k]

    for k in list(result_dict.keys()):
        if (k.startswith('materials') or k.startswith('options')) and ('_' in k):
            del result_dict[k]
            
    if result_dict['materials'] == {}:
        del result_dict['materials']
    if result_dict['options'] == {}:
        del result_dict['options']
            
    result_dict['addr'] = gmaps.geocode(result_dict['addr'])[0]['formatted_address']

    return result_dict
