// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
// import {ERC721} from "@rari-capital/solmate/src/tokens/ERC721.sol";

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./ERC721A.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/interfaces/IERC165.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

contract Tiger is Ownable, ERC721A, ReentrancyGuard {
    uint256 public immutable amountReservedForWhitelisted;

    struct SaleConfig {
        uint64 publicPrice;
    }

    SaleConfig public saleConfig;

    mapping(address => uint256) public allowlist;

    constructor(
        uint256 maxBatchSize_, //10
        uint256 collectionSize_, // 2000
        uint256 amountReservedForWhitelisted_ // 1000
    ) ERC721A("Tiger", "TGR", maxBatchSize_, collectionSize_) {
        amountReservedForWhitelisted = amountReservedForWhitelisted_;

        require(
            amountReservedForWhitelisted <= collectionSize_,
            "larger collection size needed"
        );
    }

    // whitelisting

    mapping(address => bool) whitelistedAddresses;
    uint256 public mintedByWhitelist;

    function addUser(address _addressToWhitelist) public onlyOwner {
        whitelistedAddresses[_addressToWhitelist] = true;
    }

    function verifyUser(address _whitelistedAddress)
        public
        view
        returns (bool)
    {
        bool userIsWhitelisted = whitelistedAddresses[_whitelistedAddress];
        return userIsWhitelisted;
    }

    modifier isWhitelisted() {
        require(whitelistedAddresses[msg.sender], "You need to be whitelisted");
        _;
    }
    // original contract

    modifier callerIsUser() {
        require(tx.origin == msg.sender, "The caller is another contract");
        _;
    }

    function whiteListedMint()
        external
        payable
        isWhitelisted
        nonReentrant
        returns (uint256 tokenId)
    {
        tokenId = totalSupply();
        require(
            mintedByWhitelist + 1 <= amountReservedForWhitelisted,
            "out of tokens reserved for whitelisted folks"
        );
        _safeMint(msg.sender, 1);
        whitelistedAddresses[msg.sender] = false;
        mintedByWhitelist += 1;
        return tokenId;
    }

    function publicMint() external payable callerIsUser nonReentrant {
        uint256 price = uint256(saleConfig.publicPrice);
        require(totalSupply() + 1 <= collectionSize, "reached max supply");
        require(
            totalSupply() + 1 <=
                collectionSize -
                    (amountReservedForWhitelisted - mintedByWhitelist),
            "you're minting into the whitelist reserves"
        );
        require(msg.value >= price, "you're not paying enough");
        _safeMint(msg.sender, 1);
    }

    // // metadata URI
    string private _baseTokenURI;

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseTokenURI;
    }

    function setBaseURI(string calldata baseURI) external onlyOwner {
        _baseTokenURI = baseURI;
    }

    function withdrawMoney() external onlyOwner nonReentrant {
        (bool success, ) = msg.sender.call{value: address(this).balance}("");
        require(success, "Transfer failed.");
    }

    function setOwnersExplicit(uint256 quantity)
        external
        onlyOwner
        nonReentrant
    {
        _setOwnersExplicit(quantity);
    }

    function numberMinted(address owner) public view returns (uint256) {
        return _numberMinted(owner);
    }

    function getOwnershipData(uint256 tokenId)
        external
        view
        returns (TokenOwnership memory)
    {
        return ownershipOf(tokenId);
    }

    // Settting royalties

    // Mappings _tokenID -> values
    mapping(uint256 => address) receiver;
    mapping(uint256 => uint256) royaltyPercentage;

    // Set to be internal function _setReceiver
    function _setReceiver(uint256 _tokenId, address _address) public onlyOwner {
        receiver[_tokenId] = _address;
    }

    // Set to be internal function _setRoyaltyPercentage
    function _setRoyaltyPercentage(uint256 _tokenId, uint256 _royaltyPercentage)
        public
        onlyOwner
    {
        royaltyPercentage[_tokenId] = _royaltyPercentage;
    }

    // Override for royaltyInfo(uint256, uint256)
    function royaltyInfo(uint256 _tokenId, uint256 _salePrice)
        public
        view
        override
        returns (address Receiver, uint256 royaltyAmount)
    {
        Receiver = receiver[_tokenId];
        royaltyAmount = (_salePrice * royaltyPercentage[_tokenId]) / 100;
        return (Receiver, royaltyAmount);
    }

    // Merkle stuff
    string merkleRoot = "91368911a948c0e33951fc0cab91ea82";

    // Generate the leaf node (just the hash of tokenID concatenated with the account address)
    // function _leaf(address account, uint256 tokenId)
    //     internal
    //     pure
    //     returns (bytes32)
    // {
    //     return keccak256(abi.encodePacked(tokenId, account));
    // }

    // // Verify that a given leaf is in the tree.
    // function _verify(bytes32 _leafNode, bytes32[] memory proof)
    //     internal
    //     view
    //     returns (bool)
    // {
    //     return MerkleProof.verify(proof, merkleRoot, _leafNode);
    // }

    // function mintWhitelist(
    //     address account,
    //     uint256 tokenId,
    //     bytes32[] calldata proof
    // ) public payable {
    //     require(_verify(_leaf(account, tokenId), proof), "Invalid proof");
    //     // Require that this token or wallet hasn't already minted
    //     // Store that either the wallet or tokenID has been minted, then mint the token
    // }
}
