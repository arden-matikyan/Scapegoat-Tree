Note: The standard scapegoat tree uses α = 2/3 but the generalized version may be initialized
with α = a/b where 1/2 < a/b < 1. Keep in mind that this α value impacts the rebalancing several
ways. In addition the tree will store string values as well as keys, just like the AVL tree project.
As with the B-tree project we have implemented a SGtree class as well as a Node class. The SGtree
class stores the a and b values as well as a pointer to the root Node. The various functions are then
implemented as methods of the SGtree class.

Details

The functions should do the following:

• def insert(self, key: int, value: str):

Insert the key,value pair into the tree and rebalance as per scapegoat tree rules. The key is
guaranteed not to be in the tree.

• def delete(self, key: int):

Delete the key,value pair from the tree and rebalance as per scapegoat tree rules. The key is
guaranteed to be in the tree.

• def search(self, search_key: int) -> str:

Calculate the list of values on the path from the root to the search key, including the value
associated to the search key. Return the json stringified list. The key is guaranteed to be in
the tree.
