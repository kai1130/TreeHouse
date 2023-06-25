import credentials as c
from flask import Flask, jsonify, request
import os
import credentials as c
from src.services import DBService as dbs
from src.services import SmartContractService as smartc
from src.utils import dataFormatter as df
from web3 import Web3
import json
from src.constants.sampleData import sample_data_3
from src.services.GraphingService import GraphingService as gs


with open("./contract_bytecode/generic_controller/generic_abi.json") as abi_fil:
    controller_abi = json.loads(abi_fil.read())

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
    os.environ["CONTRACT_EVM_ADDR"] = c.CONTRACT_EVM_ADDR
    
except:
    print ("ENVIRONMENT NOT SET.  PLEASE SET credentials.py")
    raise Error('No ENV') 

# BEGIN FLASK LOGIC

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    return jsonify(data='foobar')

@app.route('/ping', methods=['GET', 'POST'])
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


@app.route('/platform_info')
def platform_info():
    return jsonify({
        "contract_id" : os.environ["CONTRACT_ID"],
        "contract_addr" : os.environ["CONTRACT_EVM_ADDR"],
        "contract_abi" : controller_abi
    })


@app.route('/registry/all', methods=["GET"])
def getAllRegistryInfo():

    data_format = request.args.get('format')

    SmartContractService = smartc.ContractService(
        f'{c.JSON_RPC}/{c.ARKHIA_KEY}',
        c.CONTRACT_EVM_ADDR,
        controller_abi
    )

    reg_materials = SmartContractService.grabAllRegisteredMaterials()
    
    if data_format and data_format == "object":
        return jsonify({"data": df.convertContractArrayToOptionsStruct(reg_materials)})
    else:
        return jsonify({"data": reg_materials})


@app.route('/registry/routes', methods=['GET'])
def getCoordinatesFromRegistry():
    SmartContractService = smartc.ContractService(
        f'{c.JSON_RPC}/{c.ARKHIA_KEY}',
        c.CONTRACT_EVM_ADDR,
        controller_abi
    )

    reg_materials = SmartContractService.grabAllRegisteredMaterials()
    
    
    config = {"data": df.convertContractArrayToOptionsStruct(reg_materials)}

@app.route('/registry/create_car', methods=['POST'])
def createCar():
    car_name = request.form.get('name')
    model = request.form.get('model')
    options = json.loads(request.form.get('options')) # [ {type: <Option_Type>, name: <Option_Name>}, {type: <Option_Type>, name: <Option_Name>}]
    user_location = request.form.get('user_location')
    
    print(model)
    print(options)

    SmartContractService = smartc.ContractService(
        f'{c.JSON_RPC}/{c.ARKHIA_KEY}',
        c.CONTRACT_EVM_ADDR,
        controller_abi
    )

    reg_materials = SmartContractService.grabAllRegisteredMaterials()
    
    
    config =  df.convertContractArrayToOptionsStruct(reg_materials)

    car = gs(config)
    car.select_model(model)

    for opt in options:
        car.select_option(opt["type"], opt["name"])
    
    car.set_name(car_name)
    car.set_coords()
    car.set_location(user_location or None)
    car.sum_mat()
    car.get_cumul_weight()
    car.get_nodes()
    car.calc_edges()

    return jsonify({"data": car.generatePlot()})




if __name__ == '__main__':
    app.run()