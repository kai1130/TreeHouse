// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

contract TreeHouseAspectController {

    struct Attributes {
        string name;
        string category;
        uint256 price;
        string manufacturer;
        string addr;
        uint256 weight;
        uint256 materials_metal;
        uint256 materials_plastic;
        uint256 options_seats;
        uint256 options_wheels;
    }

    event aspectCreated(uint256 aspectIndex);

    mapping (uint256 => Attributes) Aspects;
    uint256 aspectCount = 0; // Note there will be no 0 Aspect.  A 0 aspect is equivalent to null
    address owner;

    constructor() {
      owner = msg.sender;
    }

    function createNewAspect(        
        string memory name,
        string memory category,
        uint64 price,
        string memory manufacturer,
        string memory addr,
        uint64 weight,
        uint64 materials_metal,
        uint64 materials_plastic,
        uint256 options_seats, // IDX of pertinent Aspect
        uint256 options_wheels // IDX of pertinent Aspect
    ) public returns (uint256)
    {
      aspectCount += 1;
      Aspects[aspectCount] = Attributes(
        name, 
        category,
        price, 
        manufacturer, 
        addr, 
        weight, 
        materials_metal, 
        materials_plastic, 
        options_seats, 
        options_wheels
     );

     emit aspectCreated(aspectCount);

     return aspectCount;
    }

    function getAspect(uint256 idx) public view returns (Attributes memory) {
        return Aspects[idx];
    }

    function getAspectCount()public view returns (uint256) {
        return aspectCount;
    }

    function getOwner() public view returns (address) {
        return owner;
    }
}
