import merkletools

mt = merkletools.MerkleTools(hash_type="md5")  # default is sha256 

whitelisted_addresses = [
    '0x8C53226fb89A2B88fc51b80C240D96aec10996b4',
    '0x8C53226fb89A2B88fc51b80C240D96aec10996b1',
    '0x8C53226fb89A2B88fc51b80C240D96aec10993b4',
    '0x8C53226fb89A2B88fc51b80C240D96aec10993b4',
]

for i in range(0, len(whitelisted_addresses)):
    mt.add_leaf(whitelisted_addresses, True)

mt.make_tree()

root_value = mt.get_merkle_root()

print(root_value)


