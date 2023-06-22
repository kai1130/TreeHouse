pragma solidity ^0.8.0;

contract Model_A {

    struct attributes {
        string name;
        uint256 price;
        string manufacturer;
        string addr;
        uint256 weight;
        uint256 materials_metal;
        uint256 materials_plastic;
        string options_seats;
        string options_wheels;
    }

   attributes public attr;

   constructor() {
      attr.name = "Model A";
      attr.price = 50000;
      attr.manufacturer = "Hedera Motors Dallas";
      attr.addr = "2400 Aviation Dr, DFW Airport, TX 75261, USA";
      attr.weight = 1800;
      attr.materials_metal = 1300;
      attr.materials_plastic = 700;
      attr.options_seats = "";
      attr.options_wheels = "";
    }
}
