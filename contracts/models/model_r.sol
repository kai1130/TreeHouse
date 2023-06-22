pragma solidity ^0.8.0;

contract Model_R {

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
      attr.name = "Model R";
      attr.price = 80000;
      attr.manufacturer = "Hedera Motors Hangzhou";
      attr.addr = "6CPQ+9HC, Xiaoshan District, Hangzhou, Zhejiang, China";
      attr.weight = 2100;
      attr.materials_metal = 1500;
      attr.materials_plastic = 800;
      attr.options_seats = "";
      attr.options_wheels = "";
    }
}
