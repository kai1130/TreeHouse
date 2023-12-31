pragma solidity ^0.8.0;

contract w19 {

    struct attributes {
        string name;
        uint64 price;
        string manufacturer;
        string addr;
        uint64 weight;
        uint64 materials_rubber;
        uint64 materials_metal;
    }

   attributes public attr;

    constructor() {
       attr.name = "W19";
       attr.price = 1000;
       attr.manufacturer = "Berlin Wheel Company Ltd";
       attr.addr = "Melli-Beese-Ring 1, 12529 Schonefeld";
       attr.weight = 100;
       attr.materials_rubber = 11;
       attr.materials_metal = 38;
    }
}
