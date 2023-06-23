pragma solidity ^0.8.0;

contract Model_B {

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
        attr.name = "Model B";
        attr.price = 70000;
        attr.manufacturer = "Hedera Motors Hangzhou";
        attr.addr = "6CPQ+9HC, Xiaoshan District";
        attr.weight = 1800;
        attr.materials_metal = 1100;
        attr.materials_plastic = 500;
        attr.options_seats = "";
        attr.options_wheels = "";
    }
}
