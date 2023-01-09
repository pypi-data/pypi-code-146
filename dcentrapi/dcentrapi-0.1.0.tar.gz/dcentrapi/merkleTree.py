# import requests
# from eth_abi import encode
# from web3 import Web3
# from dcentrapi.Base import Base
#
#
# class MerkleTreeNode:
#     def __init__(self, value):
#         self.left = None
#         self.right = None
#         self.value = value
#         self.hashValue = Web3.solidityKeccak(["bytes"], [value])
#
#
# def verify_leaf(root: str, leaf: tuple, proof: list, encoding: str) -> bool:
#     encoded_leaf = encode([encoding], [leaf])
#     computed_hash = MerkleTreeNode(value=encoded_leaf).hashValue
#     for proof_elem in proof:
#
#         if computed_hash <= proof_elem:
#             encoded = encode(["(bytes32,bytes32)"], [(computed_hash, proof_elem)])
#         else:
#             encoded = encode(["(bytes32,bytes32)"], [(proof_elem, computed_hash)])
#         computed_hash = MerkleTreeNode(value=encoded).hashValue
#
#     return computed_hash.hex() == root
#
#
# class MerkleTree(Base):
#
#     def __init__(self, stage, username, key):
#         super().__init__(stage, username, key)
#         url = "https://test-api.dcentralab.com/auth"
#
#         response = requests.get(url, headers=self.headers)
#         if response.status_code != 200:
#             raise "Unauthorized, MerkleTree instance cannot be used"
#
#     nodes = []
#     layers = []
#     leaf_index_map = {}
#
#     def build_tree(self, leaves, encoding):
#         if len(leaves) == 0:
#             raise "no leaves, aborting"
#
#         self.nodes = []
#         for i in range(len(leaves)):
#             leaf = leaves[i]
#             encoded_leaf = encode([encoding], [leaf])
#             self.nodes.append(MerkleTreeNode(encoded_leaf))
#             self.leaf_index_map[leaf] = i
#         self.layers = [self.nodes]
#
#         while len(self.nodes) != 1:
#             temp = []
#             for i in range(0, len(self.nodes), 2):
#                 node1 = self.nodes[i]
#                 if i + 1 < len(self.nodes):
#                     node2 = self.nodes[i + 1]
#                 else:
#                     temp.append(self.nodes[i])
#                     break
#                 if node1.hashValue <= node2.hashValue:
#                     encoded = encode(["(bytes32,bytes32)"], [(node1.hashValue, node2.hashValue)])
#                 else:
#                     encoded = encode(["(bytes32,bytes32)"], [(node2.hashValue, node1.hashValue)])
#
#                 parent = MerkleTreeNode(encoded)
#
#                 parent.left = node1
#                 parent.right = node2
#                 temp.append(parent)
#             self.nodes = temp
#             self.layers.append(temp)
#         return self.nodes[0], self.layers
#
#     def get_proof(self, leaf: tuple) -> [MerkleTreeNode]:
#         proof = []
#         index = self.leaf_index_map[leaf]
#         for layer in self.layers:
#             is_right_node = index % 2
#             pair_index = index - 1 if is_right_node else index + 1
#
#             if pair_index < len(layer):
#                 proof.append(layer[pair_index])
#
#             index = int(index / 2)
#
#         return proof
#
#
