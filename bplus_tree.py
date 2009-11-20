#!/usr/bin/env python2.4

DEFAULT_ORDER = 200

if DEFAULT_ORDER < 0:
    DEFAULT_ORDER = 2

class leaf_node(object):
    def __init__(self,order):
        self.order = order
        self.left = None
        self.right = None
        self.keys = []
        self.mapping = {}

    def insert(self,newkey,newvalue):
        if newkey in self.keys:
            return None
        # find the needed position
        pos = 0
        while pos < len(self.keys):
            if self.keys[pos] > newkey:
                break
            pos += 1
        
        # put the new key in the right place
        self.keys.insert(pos,newkey)
        self.mapping[newkey] = newvalue

        # did we overfill this node?
        if len(self.keys) > self.order:
            # we need to split this node
            mid = len(self.keys) // 2
            left = self.keys[:mid]
            right = self.keys[mid:]

            # create a new leaf
            new_leaf = leaf_node(order=self.order)

            # set the keys
            new_leaf.keys = right
            self.keys = left
            for k in new_leaf.keys:
                new_leaf.mapping[k] = self.mapping[k]
                del self.mapping[k]

            # set the left/right links
            new_leaf.right = self.right
            self.right = new_leaf
            new_leaf.left = self

            # send back the new leaf
            return (self,new_leaf)
        else:
            # we had room for the new key
            return None

    def remove(self,key):
        if key in self.keys:
            self.keys.pop(self.keys.index(key))
            del self.mapping[key]

    def __str__(self):
        return 'Leaf: %s' % self.keys

    def __repr__(self):
        return str(self)

class interior_node(object):
    def __init__(self,order):
        self.keys = []
        self.order = order
        self.children = []

    def insert(self,newkey,newvalue):
        # find the needed position
        pos = 0
        while pos < len(self.keys):
            if self.keys[pos] > newkey:
                break
            pos += 1

        # put the key in the right place
        ret = self.children[pos].insert(newkey,newvalue)

        if ret != None:
            # the child split, we have to handle it
            old_child,new_child = ret

            # first, add the returned nodes to my children list
            self.children[pos] = old_child
            self.children.insert(pos+1,new_child)

            # then add the new child's first key to my key list
            current = new_child
            while not isinstance(current,leaf_node):
                current = current.children[0]
            self.keys.insert(pos,current.keys[0])

            # did this mucking make me too big?
            if len(self.keys) > self.order:
                # we need to split
                mid = len(self.keys) // 2
                left = self.keys[:mid]
                right = self.keys[mid+1:]

                # create a new interior node
                new_node = interior_node(order=self.order)

                # set the keys
                new_node.keys = right
                self.keys = left

                # set the children
                for i in range(mid+1,len(self.children)):
                    new_node.children.append(self.children[i])
                for i in range(len(self.children)-1,mid,-1):
                    self.children.pop(i)

                # send back the new nodes
                return (self,new_node)
            else:
                # I had room to grow, everything is ok
                return None
        else:
            # there was enough room for the element somewhere below me
            return None

    def remove(self,key):
        # the key is not in this node, but it may be in a child node
        pos = 0
        while pos < len(self.keys):
            if self.keys[pos] > key:
                break
            pos += 1
        self.children[pos].remove(key)
        
        if len(self.children[pos].keys) <= 0:
            if pos >= len(self.children)-1:
                n = pos-1
            else:
                n = pos+1
            c1 = self.children[pos]
            c2 = self.children[n]
            total_keys = c1.keys + c2.keys
            if isinstance(c1,leaf_node):
                total_mapping = {}
                for k,v in c1.mapping.items():
                    total_mapping[k] = v
                for k,v in c2.mapping.items():
                    total_mapping[k] = v
            mid = len(total_keys) // 2
            left = total_keys[:mid]
            right = total_keys[mid:]
            c1.keys = left
            c2.keys = right
            if isinstance(c1,leaf_node):
                for k in c1.keys:
                    c1.mapping[k] = total_mapping[k]
                for k in c2.keys:
                    c2.mapping[k] = total_mapping[k]
            self.children[pos] = c1
            self.children[n] = c2

        current = self.children[min(len(self.children)-1,pos+1)]
        while not isinstance(current,leaf_node):
            current = current.children[0]
        self.keys[min(len(self.keys)-1,pos)] = current.keys[0]

    def __str__(self):
        return 'Keys: %s Children: %s' % (self.keys,self.children)

    def __repr__(self):
        return str(self)

class bplus_tree(object):
    def __init__(self,order=None):
        self.order = order or DEFAULT_ORDER
        self.root = None

    def insert(self,newkey,newvalue):
        # start the tree if necessary
        if self.root is None:
            self.root = leaf_node(self.order)

        # insert the key and value
        ret = self.root.insert(newkey,newvalue)

        # did the child split?
        if ret != None:
            old_child,new_child = ret
            new_root = interior_node(self.order)
            current = new_child
            while not isinstance(current,leaf_node):
                current = current.children[0]
            new_root.keys = [current.keys[0]]
            new_root.children.append(old_child)
            new_root.children.append(new_child)
            self.root = new_root

    def remove(self,key):
        raise NotImplementedError, 'remove() does not work at this time'
        if self.root is None:
            return
        self.root.remove(key)
        if len(self.root.keys) <= 0:
            self.root = None

    def inOrder(self):
        if self.root is None:
            return
        # go down the left child until we find a leaf
        current = self.root
        while not isinstance(current,leaf_node):
            current = current.children[0]
        
        # now start traversing across all the leaf nodes
        while current is not None:
            for k in current.keys:
                yield current.mapping[k]
            current = current.right
            
    def values(self):
        return list(self.inOrder())
        
    itervalues = inOrder

    def keys(self):
        return list(self.iterkeys())

    def iterkeys(self):
        if self.root is None:
            return
        # go down the left child until we find a leaf
        current = self.root
        while not isinstance(current,leaf_node):
            current = current.children[0]
        
        # now start traversing across all the leaf nodes
        while current is not None:
            for k in current.keys:
                yield k
            current = current.right

    def items(self):
        items = []
        if self.root is None:
            return items
        # go down the left child until we find a leaf
        current = self.root
        while not isinstance(current,leaf_node):
            current = current.children[0]
        
        # now start traversing across all the leaf nodes
        while current is not None:
            for k in current.keys:
                items.append((k,current.mapping[k]))
            current = current.right
        return items

    def iteritems(self):
        if self.root is None:
            return
        # go down the left child until we find a leaf
        current = self.root
        while not isinstance(current,leaf_node):
            current = current.children[0]
        
        # now start traversing across all the leaf nodes
        while current is not None:
            for k in current.keys:
                yield (k,current.mapping[k])
            current = current.right

    def has_key(self,key):
        return key in self

    def get(self,key,default=None):
        try:
            return self[key]
        except:
            return default

    def find(self,key):
        if self.root is None:
            raise AttributeError, 'bplus_tree instance has no attribute %s' % key
        current = self.root
        while not isinstance(current,leaf_node):
            pos = 0
            while pos < len(current.keys):
                if current.keys[pos] > key:
                    break
                pos += 1
            current = current.children[pos]
        if key in current.keys:
            return current.mapping[key]
        else:
            return current

    def __contains__(self,key):
        return self.get(key) != None

    def __setitem__(self,key,value):
        return self.insert(key,value)
        
    def __getitem__(self,key):
        ret = self.find(key)
        if isinstance(ret,leaf_node):
            raise AttributeError, 'bplus_tree instance has no attribute %s' % key
        else:
            return ret

    def __delitem__(self,key):
        return self.remove(key)
        
    def __str__(self):
        return 'B+ tree: %s' % self.root

    def __repr__(self):
        return str(self)
        
if __name__ == '__main__':
    tree = bplus_tree(2)
    max = 3
    l = range(1,max+1)
    for i in l:
        k = str(i)
        while len(k) < len(str(max)):
            k = '0' + k
        v = i
        tree[k] = v
    print tree
    for i in l:
        k = str(i)
        del tree[k]
        print k,tree
