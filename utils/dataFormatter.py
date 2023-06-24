
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
    0 # seats
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


