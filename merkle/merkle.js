import { ethers } from "ethers";
import keccak256 from "keccak256";
import MerkleTree from "merkletreejs";
// Map tokenID to wallets
// e.g.

const tokens = {
    2: "0xabcde..."
}

export function hashToken(tokenId, account) {
    return Buffer.from(ethers.utils.solidityKeccak256(["uint256", "address"], [tokenId, account]).slice(2), "hex");
}

export function generateMerkleTree() {
    const merkleTree = new MerkleTree(
        Object.entries(tokens).map((token) => hashToken(...token)),
        keccak256,
        { sortPairs: true }
    );
    console.log(merkleTree.getHexRoot())
    return merkleTree;
}
