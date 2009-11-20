#!/usr/bin/env python


## this probably doesn't really completely work yet

class Node(object):
    def __init__(self,name):
        self.above_nodes = []
        self.below_nodes = []
        self.name = name
    def __repr__(self):
        return self.name

class NodeList(object):
    def __init__(self,*args):
        if not isinstance(args,list):
            args = list(*args)

        self.nodes = {}
        for node_name in args:
            self.nodes[node_name] = Node(node_name)

class WordDictionary(object):
    def __init__(self,words=None):
        self.node_lists = []
        if words is not None:
            for i in xrange(max(len(word) for word in words)):
                self.node_lists.insert(i,[])
                for word in words:
                    if i < len(word):
                        letter = Node(word[i])
                        try:
                            letter.above_nodes = [x for x in self.node_lists[i-1] if x.name == word[i-1]]
                            for node in letter.above_nodes:
                                if letter.name not in [x.name for x in node.below_nodes]:
                                    node.below_nodes.append(letter)
                        except:
                            pass
                        if letter.name not in (x.name for x in self.node_lists[i]):
                            self.node_lists[i].append(letter)

    def find(self,target):
        res = []
        for i,letter in enumerate(target):
            if letter not in (x.name for x in self.node_lists[i]):
                break
            res.append(letter)
        return ''.join(res)


if __name__ == '__main__':
    new_dict = WordDictionary(['cat','hat','hello'])
    print new_dict.find('hat')
    print new_dict.find('bat')
    print new_dict.find('helen')
    
    print 'loading dictionary'
    words = open('/usr/share/dict/british-english','rb').readlines()
    #new_dict = WordDictionary([x.strip() for x in words])
    import trie
    new_dict = trie.Trie()
    for i,word in enumerate(words):
        new_dict.add(word.strip().lower(),word.strip())
    print new_dict
    print 'loading text to check'
    words = open('common_sense.txt','rb').read()
    import string
    for c in string.punctuation:
        words = words.replace(c,' ')
    words = words.split()
    print 'Doing spell check'
    for word in words:
        found = new_dict.find(word.lower())
        if found is None:
            prefix,remainder = new_dict.find_prefix(word.lower())
            print '  %s (%s,%s)' % (`word`,`prefix`,`remainder`)
