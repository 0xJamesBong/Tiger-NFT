// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.10;

import "forge-std/Test.sol";
import "../TigerGDA.sol";

interface CheatCodes {
    function startPrank(address) external;

    function prank(address) external;

    function deal(address who, uint256 newBalance) external;

    function addr(uint256 privateKey) external returns (address);

    function warp(uint256) external; // Set block.timestamp
}

contract TigerTest is Test {
    Tiger tiger;
    CheatCodes cheats = CheatCodes(HEVM_ADDRESS);

    address alice = address(0xAAAA);
    address bob = cheats.addr(0xBBBB);
    address candice = cheats.addr(0xCCCC);
    address dominic = cheats.addr(0xDDDD);

    string public baseURI = "arweave.link";

    function setUp() public {
        hoax(alice);
        tiger = new Tiger("Tiger", "TGR", 3000, 500);
        assertEq(tiger.owner(), alice);
    }

    function testSetBaseURI() public {
        assertEq(tiger.baseTokenURI(), "");
        hoax(alice);
        tiger.setBaseURI(baseURI);
        assertEq(tiger.baseTokenURI(), baseURI);
    }

    function testSetRoyaltyPercent() public {
        assertEq(tiger.royaltyPercent(), 20);
        startHoax(alice);
        tiger.setRoyaltyPercent(10);
        assertEq(tiger.royaltyPercent(), 10);
    }

    function testGift() public {
        startHoax(alice);
        console.log(tiger.currentId());
        tiger.gift(10, bob);
        console.log(tiger.currentId());
        assertEq(tiger.ownerOf(1), bob);
        for (uint256 i = 1; i <= 10; i++) {
            assertEq(tiger.ownerOf(i), bob);
        }
    }

    function testSetNewGDA() public {
        int256 _initialPrice = 120;
        int256 _scaleFactor = 1;
        int256 _decayConstant = 2;
        int256 _auctionStartTime = 1;
        uint256 _amount = 100;
        hoax(alice);
        tiger.setNewGDA(
            _initialPrice,
            _scaleFactor,
            _decayConstant,
            _auctionStartTime,
            _amount
        );
        hoax(bob);

        for (uint256 i = 0; i < 10; i++) {
            vm.warp(i);
            console.log(
                "time:",
                block.timestamp,
                "the price now is:",
                tiger.purchasePrice(1)
            );

            if (i % 5 == 0) {
                tiger.purchaseTokens{value: 1000000}(1, payable(address(bob)));
                if (tiger.ownerOf(i) == bob) {
                    console.log("bought");
                }
            }
            // console.log(block.timestamp);
        }

        hoax(bob);
        // tiger.purchaseTokens()
    }

    function testAuction() public {}

    function testWithdraw() public {}

    // function testSupplyMerkleRoot() public {
    // bytes32 public root;
    // startHoax(alice);
    // tiger.supplyMerkleRoot(root);
    //
    // }

    function testWhitelistMint() public {}
}
