from flask import Flask, jsonify
import os
import credentials as c
from src.services import DBService as dbs
from web3 import Web3
import json
from src.constants.sampleData import sample_data_3

with open("./contract_bytecode/generic_controller/generic_abi.json") as abi_fil:
    controller_abi = json.loads(abi_fil.read())


print(controller_abi)

try:
    from src.services import HederaService as hs
except:
    print("Architecture Error, using PreCompile at %s" % c.CONTRACT_ID)
    os.environ["CONTRACT_ID"] = c.CONTRACT_ID



INIT_FILE = "initted"

try:
    # SETTING ENVIRON ON INIT
    os.environ["OPERATOR_ID"] = c.OPERATOR_ID
    os.environ["OPERATOR_KEY"] = c.OPERATOR_KEY
    os.environ["GMAPS_API"] = c.gmaps_api
    os.environ["ARKHIA_KEY"] = c.ARKHIA_KEY
    os.environ["JSON_RPC"] = c.JSON_RPC
    os.environ["MIRROR_NODE"] = c.MIRROR_NODE
    
    print(
        f"""
        Setting ENVIRON:
        \n{os.environ['OPERATOR_ID']}
        \n{os.environ['OPERATOR_KEY']}
        \n{os.environ['GMAPS_API']}
        \n{os.environ['ARKHIA_KEY']}
        \n{os.environ['JSON_RPC']}
        \n{os.environ['MIRROR_NODE']}
    """)
except:
    print ("ENVIRONMENT NOT SET.  PLEASE SET credentials.py")
    raise Error('No ENV') 

# BEGIN FLASK LOGIC

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify(data='foobar')

@app.route('/ping')
def ping():
    return jsonify(data='pong')

@app.route('/product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    manufacturer = request.form.get('manufacturer')
    addr = request.form.get('addr')
    weight = request.form.get('weight')
    materials_metal = request.form.get('materials_metal')
    materials_plastic = request.form.get('materials_plastic')
    options_seats = request.form.get('options_seats')
    options_wheels = request.form.get('options_wheels')

    # Perform database insertion or any other desired operation with the received data

    return jsonify(data='Product added successfully')

@app.route('/init', methods=['GET'])
def init_platform():
    pass
    # CHECK for init
    try:
      init_file = open(INIT_FILE, "r")
      if (init_file.read() == 'platform_initted'):
          return jsonify(data='Platform Already Initted')
    except:
      pass
    
    # Create Controller Contract
    if os.environ["CONTRACT_ID"]:
        print("Using PreCompile")
    else:
        with open("./contract_bytecode/generic/generic_controller.bin", "r") as my_fil:
            contract_id = hs.create_hedera_contract(my_fil.read()) # @Kai: Untested in dev env
            os.environ["CONTRACT_ID"] = contract_id
    
    # Create Tables in DB
    database = dbs.SQLiteWrapper('treehouse.db')
    database.create_product_table()
    database.create_contract_table()

    # Write Controller Contract Reference into DB
    database.insert_contract(os.environ["CONTRACT_ID"],296)

    # Seed Contract
    #provider_string = f"{os.environ['JSON_RPC']}/{os.environ['ARKHIA_KEY']}"
    provider_string = c.TESTNET_HASHIO_RPC
    w3 = Web3(Web3.HTTPProvider(provider_string))

    print("Chain ID: %s" % w3.eth.chain_id)
    

    treehouse_controller = w3.eth.contract(
        address = c.CONTRACT_EVM_ADDR,
        abi = controller_abi
    )

    for sample in sample_data_3:
        nonce = w3.eth.get_transaction_count(c.OPERATOR_EVM_ADDR) 

        tx_call = treehouse_controller.functions.createNewAspect(
            sample["name"],
            sample["category"],
            sample["price"],
            sample["manufacturer"],
            sample["addr"],
            sample["weight"],
            sample["metal"],
            sample["plastic"],
            sample["seats"],
            sample["wheels"]
        ).build_transaction({'chainId' : 296, 'nonce' : nonce})

        signed_tx = w3.eth.account.sign_transaction(tx_call, c.OPERATOR_EVM_KEY)

        print(signed_tx)

        w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print("TX CALL")
        print(tx_call)

    # Finally...
    init_file = open(INIT_FILE, "w")
    init_file.close()


if __name__ == '__main__':
    app.run()