pragma solidity ^0.8.0;

contract w18 {

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
       attr.name = "W18";
       attr.price = 0;
       attr.manufacturer = "Shanghai Wheel Company Ltd";
       attr.addr = "4RV5+P8J, Yingbin Expy, Pudong";
       attr.weight = 90;
       attr.materials_rubber = 10;
       attr.materials_metal = 36;
    }
}
