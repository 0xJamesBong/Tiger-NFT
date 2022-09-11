// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
// import {ERC721} from "@rari-capital/solmate/src/tokens/ERC721.sol";

import {Owned} from "solmate/src/auth/Owned.sol";
import {ReentrancyGuard} from "@rari-capital/solmate/src/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/interfaces/IERC165.sol";
// import "./DiscreteGDA.sol";
import {ERC721} from "@rari-capital/solmate/src/tokens/ERC721.sol";
import {PRBMathSD59x18} from "@prb/math/contracts/PRBMathSD59x18.sol";
import {MerkleProofLib} from "solmate/src/utils/MerkleProofLib.sol";

contract Tiger is ERC721, Owned, ReentrancyGuard {
    using PRBMathSD59x18 for int256;
    using MerkleProofLib for bytes32[];

    // 2000 NFTs
    uint256 public immutable collectionSize;
    uint256 public immutable amountReservedForWhitelisted;

    // To be replaced by Merkleroot
    // mapping(address => uint256) public allowlist;

    constructor(
        string memory _name,
        string memory _symbol,
        uint256 _collectionSize, // 2000
        uint256 _amountReservedForWhitelisted // 1000
    ) ERC721(_name, _symbol) Owned(msg.sender) {
        collectionSize = _collectionSize;
        amountReservedForWhitelisted = _amountReservedForWhitelisted;
    }

    ///@notice parameter that controls initial price, stored as a 59x18 fixed precision number
    int256 internal initialPrice;

    ///@notice parameter that controls how much the starting price of each successive auction increases by,
    // stored as a 59x18 fixed precision number
    int256 internal scaleFactor;

    ///@notice parameter that controls price decay, stored as a 59x18 fixed precision number
    int256 internal decayConstant;

    ///@notice start time for all auctions, stored as a 59x18 fixed precision number
    int256 internal auctionStartTime;

    error InsufficientPayment();

    error UnableToRefund();

    error AuctioningOffTooMany();

    error PurchasingTooMany();

    error AuctionAlreadyInProgress();

    error GiftingTooMany();

    error NonExistentTokenURI();

    error NoEthBalance();

    error NotWithdrawn();

    // Whitelisting

    // Setting up GDA for a bunch of tokens

    ///@notice id of current ERC721 being minted
    uint256 public currentId = 0;

    ///@notice number of tokens to be auctioned off in the on-going auction
    uint256 public auctionable = 0;
    ///@notice number of gifted tokens
    uint256 public gifted = 0;
    ///@notice total number of tokens already auctioned or auctionable
    uint256 public auctioned = 0;

    ///@notice basicTokenURI
    string public baseTokenURI;

    function setNewGDA(
        int256 _initialPrice,
        int256 _scaleFactor,
        int256 _decayConstant,
        int256 _auctionStartTime,
        uint256 _amount
    ) public onlyOwner nonReentrant {
        initialPrice = _initialPrice;
        scaleFactor = _scaleFactor;
        decayConstant = _decayConstant;
        auctionStartTime = _auctionStartTime;
        if (auctionable != 0) {
            revert AuctionAlreadyInProgress();
        }
        if (amountReservedForWhitelisted + _amount + gifted > collectionSize) {
            revert AuctioningOffTooMany();
        } else {
            auctionable = _amount;
            auctioned += _amount;
            emit AuctionStarted(
                initialPrice,
                scaleFactor,
                decayConstant,
                auctionStartTime,
                auctionable
            );
        }
    }

    event AuctionStarted(
        int256 _initialPrice,
        int256 _scaleFactor,
        int256 _decayConstant,
        int256 _auctionStartTime,
        uint256 _amount
    );

    // Function to receive Ether. msg.data must be empty
    receive() external payable {}

    // Fallback function is called when msg.data is not empty
    fallback() external payable {}

    function gift(uint256 numTokens, address to)
        public
        payable
        onlyOwner
        nonReentrant
    {
        if (
            collectionSize -
                (gifted +
                    auctioned +
                    amountReservedForWhitelisted +
                    numTokens) <
            0
        ) {
            revert GiftingTooMany();
        }

        for (uint256 i = 0; i < numTokens; i++) {
            _mint(to, ++currentId);
        }
        gifted += numTokens;
    }

    ///@notice purchase a specific number of tokens from the GDA
    function purchaseTokens(uint256 numTokens, address to)
        public
        payable
        nonReentrant
    {
        uint256 cost = purchasePrice(numTokens);
        if (auctionable < numTokens) {
            revert PurchasingTooMany();
        }

        if (msg.value < cost) {
            revert InsufficientPayment();
        }
        //mint all tokens
        for (uint256 i = 0; i < numTokens; i++) {
            _mint(to, ++currentId);
        }
        //refund extra payment
        uint256 refund = msg.value - cost;
        (bool sent, ) = msg.sender.call{value: refund}("");
        // if (!sent) {
        // revert UnableToRefund();
        // } else {
        auctionable -= numTokens;
        // }
    }

    ///@notice calculate purchase price using exponential discrete GDA formula
    function purchasePrice(uint256 numTokens) public view returns (uint256) {
        int256 quantity = int256(numTokens).fromInt();
        int256 numSold = int256(currentId).fromInt();
        int256 timeSinceStart = int256(block.timestamp).fromInt() -
            auctionStartTime;

        int256 num1 = initialPrice.mul(scaleFactor.pow(numSold));
        int256 num2 = scaleFactor.pow(quantity) - PRBMathSD59x18.fromInt(1);
        int256 den1 = decayConstant.mul(timeSinceStart).exp();
        int256 den2 = scaleFactor - PRBMathSD59x18.fromInt(1);
        int256 totalCost = num1.mul(num2).div(den1.mul(den2));
        //total cost is already in terms of wei so no need to scale down before
        //conversion to uint. This is due to the fact that the original formula gives
        //price in terms of ether but we scale up by 10^18 during computation
        //in order to do fixed point math.
        return uint256(totalCost);
    }

    //////////////////////////////////////////////////////////////////////////////////////////
    // * Token URI  *
    //////////////////////////////////////////////////////////////////////////////////////////
    function setBaseURI(string memory baseTokenURI_) public onlyOwner {
        baseTokenURI = baseTokenURI_;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        string memory baseURI = baseTokenURI;
        if (ownerOf[tokenId] == address(0)) {
            revert NonExistentTokenURI();
        }
        return (
            bytes(baseURI).length > 0
                ? string(
                    abi.encodePacked(
                        baseURI,
                        Strings.toString(tokenId),
                        ".json"
                    )
                )
                : ""
        );
    }

    //////////////////////////////////////////////////////////////////////////////////////////
    // * Royalties and Balances  *//
    //////////////////////////////////////////////////////////////////////////////////////////
    /// @notice Withdraw all ETH from the contract to the vault addres.
    function withdraw() public onlyOwner {
        if (address(this).balance == 0) {
            revert NoEthBalance();
        }
        (bool sent, ) = address(owner).call{value: address(this).balance}("");
        if (!sent) {
            revert NotWithdrawn();
        }
    }

    function viewBalance() public view returns (uint256 balance) {
        return (address(this).balance);
    }

    // Royalties
    uint256 public royaltyPercent = 20;

    function setRoyaltyPercent(uint256 newRoyaltyPercent) public onlyOwner {
        royaltyPercent = newRoyaltyPercent;
    }

    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        public
        view
        returns (address receiver, uint256 royaltyAmount)
    {
        receiver = owner;
        royaltyAmount = uint256(int256(royaltyPercent * salePrice).div(100));
    }

    //////////////////////////////////////////////////////////////////////////////////////////
    // * Merkleroot and whitelisting  *//
    //////////////////////////////////////////////////////////////////////////////////////////

    bytes32 public merkleRoot;

    function supplyMerkleRoot(bytes32 root) public onlyOwner {
        merkleRoot = root;
    }

    mapping(address => bool) public whitelistClaimed;

    function whitelistMint(bytes32[] calldata _merkleProof) public {
        require(!whitelistClaimed[msg.sender], "claimed alredy!");
        bytes32 leaf = keccak256(abi.encodePacked(msg.sender));
        require(
            MerkleProofLib.verify(_merkleProof, merkleRoot, leaf),
            "Invalid proof!"
        );
        whitelistClaimed[msg.sender] = true;
        _mint(msg.sender, ++currentId);
    }
}
