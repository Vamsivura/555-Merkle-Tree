import hashlib

class MerkleNode:
    """
    Stores the hash and the parent.
    """
    def __init__(self, hash):
        self.hash = hash
        self.parent = None

class MerkleTree:
    """
    Stores the leaves and the root hash of the tree.
    """
    def __init__(self, data_chunks):
        leaves = []

        for chunk in data_chunks:
            node = MerkleNode(self.compute_file_hash(chunk))
            leaves.append(node)

        self.root = self.build_merkle_tree(leaves)

    def build_merkle_tree(self, leaves):
        """
        Builds the Merkle tree from a list of leaves. In case of an odd number of leaves, the last leaf is duplicated.
        """
        num_leaves = len(leaves)
        if num_leaves == 1:
            return leaves[0]

        parents = []

        i = 0
        while i < num_leaves:
            left_child = leaves[i]
            right_child = leaves[i + 1] if i + 1 < num_leaves else left_child

            parents.append(self.create_parent(left_child, right_child))

            i += 2

        return self.build_merkle_tree(parents)

    def create_parent(self, left_child, right_child):
        """
        Creates the parent node from the children, and updates
        their parent field.
        """
        parent = MerkleNode(
            self.compute_hash(left_child.hash + right_child.hash))
        left_child.parent, right_child.parent = parent, parent

        print("Left child: {}, Right child: {}, Parent: {}".format(
            left_child.hash, right_child.hash, parent.hash))
        return parent

    @staticmethod
    def compute_file_hash(file):
        with open(file, "rb") as f:
            bytes = f.read()  # read file as bytes
            readable_hash = hashlib.md5(bytes).hexdigest();
            #print(readable_hash)
        return readable_hash

    @staticmethod
    def compute_hash(value):
        value = value.encode('utf-8')
        hashval = hashlib.md5(value).hexdigest();
        return hashval


chunks = list()
chunks.append("file1.txt")
chunks.append("file2.txt")
chunks.append("file3.txt")
chunks.append("file4.txt")
print(chunks)
merkle_tree = MerkleTree(chunks)