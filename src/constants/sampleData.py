sample_data_1 = [
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



sample_data_2 = {
    "Model": {
        "Model H": {
            "name": "Model H",
            "price": 40000,
            "manufacturer": "Hedera Motors Dallas",
            "addr": "DFW International Airport (DFW), 2400 Aviation Dr, DFW Airport, TX 75261, USA",
            "weight": 1800,
            "materials": {"metal": 1000, "plastic": 400},
            "options": {"seats": null, "wheels": null},
        },
        "Model B": {
            "name": "Model B",
            "price": 70000,
            "manufacturer": "Hedera Motors Hangzhou",
            "addr": "6CPQ+9HC, Xiaoshan District, Hangzhou, Zhejiang, China",
            "weight": 1800,
            "materials": {"metal": 1100, "plastic": 500},
            "options": {"seats": null, "wheels": null},
        },
        "Model A": {
            "name": "Model A",
            "price": 50000,
            "manufacturer": "Hedera Motors Dallas",
            "addr": "DFW International Airport (DFW), 2400 Aviation Dr, DFW Airport, TX 75261, USA",
            "weight": 1800,
            "materials": {"metal": 1300, "plastic": 700},
            "options": {"seats": null, "wheels": null},
        },
        "Model R": {
            "name": "Model R",
            "price": 80000,
            "manufacturer": "Hedera Motors Hangzhou",
            "addr": "6CPQ+9HC, Xiaoshan District, Hangzhou, Zhejiang, China",
            "weight": 2100,
            "materials": {"metal": 1500, "plastic": 800},
            "options": {"seats": null, "wheels": null},
        },
    },
    "Wheel": {
        "W18": {
            "name": "W18",
            "price": 0,
            "manufacturer": "Shanghai Wheel Company Ltd",
            "addr": "8Q334RV5+P8J, Ying Bin Gao Su Gong Lu, Pu Dong Xin Qu, China",
            "weight": 90,
            "materials": {"rubber": 10, "metal": 36},
        },
        "W19": {
            "name": "W19",
            "price": 1000,
            "manufacturer": "Berlin Wheel Company Ltd",
            "addr": "Melli-Beese-Ring 1, 12529 Sch\u00f6nefeld, Germany",
            "weight": 100,
            "materials": {"rubber": 11, "metal": 38},
        },
        "W20": {
            "name": "W20",
            "price": 2000,
            "manufacturer": "Austin Wheel Company Ltd",
            "addr": "Parking Lot A, 3600 Presidential Blvd, Austin, TX 78719, USA",
            "weight": 120,
            "materials": {"rubber": 12, "metal": 40},
        },
    },
    "Seat": {
        "Black Seat": {
            "name": "Black Seat",
            "price": 0,
            "manufacturer": "Tokyo Seat Company",
            "addr": "1-1 Furugome, Narita, Chiba 282-0004, Japan",
            "weight": 100,
            "materials": {"leather": 15, "metal": 20},
        },
        "White Seat": {
            "name": "White Seat",
            "price": 1000,
            "manufacturer": "Mexico City Seat Company",
            "addr": "Av. Capit\u00e1n Carlos Le\u00f3n, Ciudad de M\u00e9xico, CDMX, Mexico",
            "weight": 100,
            "materials": {"leather": 15, "metal": 20},
        },
    },
}