pragma solidity ^0.8.0;

contract Model_H {

    struct attributes {
        string name;
        uint64 price;
        string manufacturer;
        string addr;
        uint64 weight;
        uint64 materials_metal;
        uint64 materials_plastic;
        string options_seats;
        string options_wheels;
    }

    attributes public attr;

    constructor() {
        attr.name = "Model H";
        attr.price = 40000;
        attr.manufacturer = "Hedera Motors Dallas";
        attr.addr = "2400 Aviation Dr, DFW Airport";
        attr.weight = 1800;
        attr.materials_metal = 1000;
        attr.materials_plastic = 400;
        attr.options_seats = "";
        attr.options_wheels = "";
    }
}
