from __future__ import annotations
import json
import math
from typing import List

# Node Class
# You may make minor modifications.

# Take standard BST code for starters.
# Write the restructuring code.  Test it on some trees by hand. It should be pretty easy to get this running independently of everything else. Check by hand.
# Write the code which monitors depth of the inserted node and compares it against the relevant value which triggers a scapegoat search. Check by hand.
# Write the code which finds a scapegoat. Check by hand.
# Link the code which finds a scapegoat to the restructuring code.
# Now you should pass all insert-only tests.
# Write the delete code.


class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# Scapegoat Tree Class.
# DO NOT MODIFY.
class SGtree():
    def  __init__(self,
                  a    : int  = None,
                  b    : int  = None,
                  m    : int  = None,
                  n    : int  = None,
                  root : Node = None):
        self.m     = 0
        self.n     = 0
        self.a     = a
        self.b     = b
        self.root  = None

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "k": node.key,
                "v": node.value,
                "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)


    def restructure(self, root: Node) -> Node:


      #print(f'restruct at: {root.key}')
        # ===================================================================
        def inorder(current: Node): 
            if current is not None and current is not root.parent:
                inorder(current.leftchild)
                keys.append(current.key)
                vals.append(current.value)
                inorder(current.rightchild)
            return 
        # =================================================================== 

        # Node: key, value, leftchild, rightchild, parent 
        # =================================================================== 
        def newBST(keyList: [int], valList: [str]) -> Node:
        
            if not keyList:
                return None
        
            # find middle index
            mid = (len(keyList)) // 2
        
            # make the middle element the root
            root = Node(keyList[mid], valList[mid], None, None, None)
        
            # left subtree of root has all
            # values <arr[mid]
            
            root.leftchild = newBST(keyList[:mid], valList[:mid])
            if root.leftchild is not None: 
                root.leftchild.parent = root 

            # right subtree of root has all
            # values >arr[mid]
            root.rightchild = newBST(keyList[mid+1:], valList[mid+1:])
            if root.rightchild is not None: 
                root.rightchild.parent = root 

            return root
        # =================================================================== 
        

        keys = [] 
        vals = [] 
        # get an inorder list of the subtree 
        inorder(root)
        newRoot = newBST(keys,vals)

        return newRoot


    # Node: key, value, leftchild, rightchild, parent 
    def insert(self, key: int, value: str):


        # goes up the tree and find which node is the scapegoat 
        def findEscape(current: Node, child: Node) -> Node:
            
            def numNodes(cur: Node) -> int: 
                if cur is None:
                    return 0 
                else:
                    return 1 + numNodes(cur.leftchild) + numNodes(cur.rightchild)

            if current.leftchild is not None and current.leftchild == child: 
                childSize = numNodes(current.leftchild)
            else: 
                childSize = numNodes(current.rightchild)
            

            currentSize = numNodes(current)

            #print(f'current: {current.key} size: {currentSize}')
            #if left:
                #print(f'leftchild: {current.leftchild.key} size: {childSize}')
            #else:
                #print(f'rightchild: {current.rightchild.key} size: {childSize}')

            if float(childSize/(currentSize)) > float(self.a/self.b):  
                scapegoat = self.restructure(current)
                #print("scapegoat found")

                if current.parent is None: 
                  #print("new root")
                    self.root = scapegoat
                else: 
                    if current.parent.leftchild is not None and current.parent.leftchild == current:
                        current.parent.leftchild = scapegoat
                        scapegoat.parent = current.parent
                    else: 
                        current.parent.rightchild = scapegoat
                        scapegoat.parent = current.parent

                return 
    
            findEscape(current.parent, current)



        #print(f'Insert: {key}') # This is just here to make the code run, you can delete it.

        self.m += 1 
        self.n += 1
        
      #print(f'Inserted, n:{self.n}  m:{self.m}')

        if self.root is None: 
            self.root = Node(key, value, None, None, None) 
            return self.root
        else:
            depth = 1
            current = self.root 
            while current is not None: 
                # print(f"going down: {current.key} and parent: {current.parent}")
                if key < current.key: 
                    if current.leftchild is None: 
                        
                        current.leftchild = Node(key, value, None, None, current)

                        # if true then there is a scapegoat at current or ancestor 
                        if depth > math.log(self.m,float(self.b/self.a)):
                            #print("scapegoat search triggered at", current.leftchild.key)
                            findEscape(current, current.leftchild)


                        return self.root 
                    else: 
                        current = current.leftchild
                        depth += 1
                elif key > current.key:
                    if current.rightchild is None: 
    
                        current.rightchild = Node(key, value, None, None, current)

                        # if true then there is a scapegoat at current or ancestor 
                        if depth > math.log(self.m,float(self.b/self.a)):

                          #print("scapegoat search triggered at", current.rightchild.key)
                          #print(depth)
                          #print(math.log(self.m,float(self.b/self.a)))
                            findEscape(current, current.rightchild)
                        
                        return self.root 
                    else: 
                        current = current.rightchild
                        depth += 1

        


    def delete(self, key: int):
        # Fill in the details.
        # print(f'Delete: {key}') # This is just here to make the code run, you can delete it.

        # =================================================================== 
        def findnext(root: Node) -> Node: 
            
            current = root 
            parent = root 
            if root.rightchild is None: 
                return None 
            else:
                parent = current 
                current = current.rightchild
                while current.leftchild is not None:
                    current = current.leftchild 

            return current 
        # =================================================================== 

        # =================================================================== 
        def deleteRecur(root: Node, key: int) -> Node:
    
            if root is None: 
                return None 
            
            # traverse until key is found 
            if key < root.key: 
                # replace key when deleted 
                root.leftchild = deleteRecur(root.leftchild, key)
                
            elif key > root.key:
                root.rightchild = deleteRecur(root.rightchild, key)
            
            else: # key is found (node to be deleted) 
                #print("Found")
                if root.leftchild is None and root.rightchild is None: 
                    root = None 
                elif root.leftchild is None:
                    repl = root.rightchild
                    if root.parent is None:
                        self.root = repl
                    repl.parent = root.parent 
                    return repl 
                elif root.rightchild is None:  
                    repl = root.leftchild
                    
                    if root.parent is None:
                        self.root = repl
                    repl.parent = root.parent 
                    return repl 
                else: 
                    
                    repl = findnext(root)
                    root.key = repl.key 
                    root.value = repl.value

                    # delete the in order successor (search by old key)
                    root.rightchild = deleteRecur(root.rightchild, repl.key)

            return root 


        if self.root.key == key and self.root.leftchild is None and self.root.rightchild is None: 
                self.root = None 
        else: 
            deleteRecur(self.root, key)
        
        self.n -= 1 
        #print(f'deleted, n:{self.n}  m:{self.m} ')

        if self.m > 2*self.n: 
          #print("restructure from root")
            newRoot = self.restructure(self.root)
            self.root = newRoot 
            self.m = self.n 
        
        return 



    def search(self, search_key: int) -> str:
            
        vals = [] 
        current = self.root
        while current is not None: 
            if search_key < current.key: 
                vals.append(current.value)
                current = current.leftchild
            elif search_key > current.key:
                vals.append(current.value)
                current = current.rightchild
            else: 
                vals.append(current.value)
                break 

        return json.dumps(vals)
