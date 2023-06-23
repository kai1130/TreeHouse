pragma solidity ^0.8.0;

contract white_seat {

    struct attributes {
        string name;
        uint256 price;
        string manufacturer;
        string addr;
        uint256 weight;
        uint256 materials_leatherette;
        uint256 materials_metal;
    }

   attributes public attr;

    constructor() {
       attr.name = "White Seat";
       attr.price = 1000;
       attr.manufacturer = "Mexico City Seat Company";
       attr.addr = "Av. Capitan Carlos Leon S/N";
       attr.weight = 100;
       attr.materials_leatherette = 15;
       attr.materials_metal = 20;
    }
}
