class Node:
    def __init__(self, val):
        self.l = None
        self.m = None
        self.r = None
        self.v = val
    
    def addLeft(self,val):
        self.l = Node(val)

    def addMid(self,val):
        self.m = Node(val)
    
    def addRight():
        self.r = Node(val)

class Tree:
    def __init__(self):
        self.root = None

    def getRoot(self):
        return self.root

    def getLeft(self):

    def setRoot(self, val):
        self.root = Node(val)


    

#     3
# 0     4
#   2      8
tree = Tree()
tree.add(3)
tree.add(4)
tree.add(0)
tree.add(8)
tree.add(2)
tree.printTree()
print((tree.find(3)).v)
print(tree.find(10))
tree.deleteTree()
tree.printTree()