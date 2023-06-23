pragma solidity ^0.8.0;

contract black_seat {

    struct attributes {
        string name;
        uint256 price;
        string manufacturer;
        string addr;
        uint256 weight;
        uint256 materials_leather;
        uint256 materials_metal;
    }

   attributes public attr;

    constructor() {
       attr.name = "Black Seat";
       attr.price = 0;
       attr.manufacturer = "Tokyo Seat Company";
       attr.addr = "1-1 Furugome, Narita, Chiba";
       attr.weight = 100;
       attr.materials_leather = 15;
       attr.materials_metal = 20;
    }
}
