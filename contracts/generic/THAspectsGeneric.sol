// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

contract TreeHouseAspectController {

    struct Attributes {
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

    mapping (uint256 => Attributes) Aspects;
    uint256 aspectCount = 0;

    constructor() {

    }

    function createNewAspect(        
        string memory name,
        uint64 price,
        string memory manufacturer,
        string memory addr,
        uint64 weight,
        uint64 materials_metal,
        uint64 materials_plastic,
        string memory options_seats,
        string memory options_wheels
    ) public returns (uint256)
    {
      aspectCount += 1;
      Aspects[aspectCount] = Attributes(
        name, 
        price, 
        manufacturer, 
        addr, 
        weight, 
        materials_metal, 
        materials_plastic, 
        options_seats, 
        options_wheels
     );

     return aspectCount;
    }

    function getAspect(uint256 idx) public view returns (Attributes memory) {
        return Aspects[idx];
    }

    function getAspectCount()public view returns (uint256) {
        return aspectCount;
    }
}
