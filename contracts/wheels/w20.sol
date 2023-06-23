pragma solidity ^0.8.0;

contract w20 {

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
       attr.name = "W20";
       attr.price = 2000;
       attr.manufacturer = "Austin Wheel Company Ltd";
       attr.addr = "3600 Presidential Blvd, Austin";
       attr.weight = 120;
       attr.materials_rubber = 12;
       attr.materials_metal = 40;
    }
}
