
INPUT_META_EXAMPLE = [
    ('Model', 'Model H', './contract_bytecode/models/model_h.bin', 'retrieve_model_dict', '0.0.14973364'),
    ('Model', 'Model B', './contract_bytecode/models/model_b.bin', 'retrieve_model_dict', '0.0.14973366'),
    ('Model', 'Model A', './contract_bytecode/models/model_a.bin', 'retrieve_model_dict', '0.0.14973368'),
    ('Model', 'Model R', './contract_bytecode/models/model_r.bin', 'retrieve_model_dict', '0.0.14973370'),
    ('Wheel', 'W18', './contract_bytecode/wheels/w18.bin', 'retrieve_wheel_dict', '0.0.14973372'),
    ('Wheel', 'W19', './contract_bytecode/wheels/w19.bin', 'retrieve_wheel_dict', '0.0.14973374'),
    ('Wheel', 'W20', './contract_bytecode/wheels/w20.bin', 'retrieve_wheel_dict', '0.0.14973376'),
    ('Seat', 'Black Seat', './contract_bytecode/seats/black_seat.bin', 'retrieve_black_seat_dict', '0.0.14973378'),
    ('Seat', 'White Seat', './contract_bytecode/seats/white_seat.bin', 'retrieve_white_seat_dict', '0.0.14973380')
]




INPUT_PRODUCT_EXAMPLE = (
    "Model B", # Name
    "Model", # Category
    70000, # Price
    "Hedera Motors Hangzhou", # Manufacturer
    "6CPQ+9HC, Xiaoshan District, Hangzhou, Zhejiang, China", # addr
    1800, # weight
    1100, # metal
    500, # plastic
    0, # seats
    0 # wheels
)


"""
tuple(string,uint64,string,string,uint64,uint64,uint64,string,string): Model B,70000,Hedera Motors Hangzhou,6CPQ+9HC, Xiaoshan District, Hangzhou, Zhejiang, China,1800,1100,500,,
"""


OUTPUT_EXAMPLE = {
        "Model B": {
            "name": "Model B",
            "price": 70000,
            "manufacturer": "Hedera Motors Hangzhou",
            "addr": "6CPQ+9HC, Xiaoshan District, Hangzhou, Zhejiang, China",
            "weight": 1800,
            "materials": {"metal": 1100, "plastic": 500},
            "options": {"seats": None, "wheels": None},
        }
}
def parseProductTuple(product_tuple):
    product_dict = {
        product_tuple[0] : {
            "name" : product_tuple[0],
            "price" : product_tuple[2],
            "manufacturer" : product_tuple[3],
            "addr" : product_tuple[4],
            "weight" : product_tuple[5],
            "metal" : product_tuple[6],
            "plastic" : product_tuple[7],
            "seats" : product_tuple[8],
            "wheels" : product_tuple[9]
        }
    }

    return (product_tuple[1], product_dict)


def assembleOptionsStructureFull(array_of_data):
    final_struct = {}

    for product_data in array_of_data:
        curr_product = parseProductTuple(product_data)
        final_struct[curr_product[0]] = curr_product[1]

    return final_struct


def determineMaterials(item_array):
    category = item_array[1] # Metal 6 Plastic 7

    if category == "Model":
        return {"metal" : item_array[6], "plastic" : item_array[7]}
    elif category == "Wheel":
        return {"metal" : item_array[6], "rubber" : item_array[7]}
    elif category == "Seat":
        return {"metal" : item_array[6], "leather" : item_array[7]}
    else:
        return {"material_a": item_array[6], "material_b" : item_array[7]}
    


def determineOptions(item_array, tuple_array):
    category = item_array[1]

    opt_1 = -1 if item_array[8] == 0 else determineMaterials(tuple_array[item_array[8]])
    opt_2 = -1 if item_array[9] == 0 else determineMaterials(tuple_array[item_array[9]])

    if category == "Model":
        return {"wheel" : opt_1, "seat" : opt_2}
    elif category == "Wheel":
        return {}
    elif category == "Seat":
        return {}
    else:
        return {"material_a": item_array[6], "material_b" : item_array[7]}

def convertContractArrayToOptionsStruct(tuple_array):
    pass

    return_obj = {}


    for item in tuple_array:
        category = item[1]
        return_obj[category] = {}

    for item in tuple_array:
        category = item[1]
        name = item[0]

        return_obj[category][name] = {
            "name" : name,
            "price" : item[2],
            "manufacturer" : item[3],
            "addr" : item[4],
            "weight" : item[5],
            "materials" : determineMaterials(item),
            "options" : determineOptions(item, tuple_array)
        }

    return return_obj
