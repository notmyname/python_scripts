# James Tauber
# http://jtauber.com/ 

class Trie:
    """
    A Trie is like a dictionary in that it maps keys to values. However,
    because of the way keys are stored, it allows look up based on the
    longest prefix that matches.
    """

    def __init__(self):
        self.root = [None, {}]


    def add(self, key, value):
        """
        Add the given value for the given key.
        """
        
        curr_node = self.root
        for ch in key:
            curr_node = curr_node[1].setdefault(ch, [None, {}])
        curr_node[0] = value


    def find(self, key):
        """
        Return the value for the given key or None if key not found.
        """
        
        curr_node = self.root
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return None
        return curr_node[0]


    def find_prefix(self, key):
        """
        Find as much of the key as one can, by using the longest
        prefix that has a value. Return (value, remainder) where
        remainder is the rest of the given string.
        """
        
        curr_node = self.root
        remainder = key
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return (curr_node[0], remainder)
            remainder = remainder[1:]
        return (curr_node[0], remainder)


    def convert(self, keystring):
        """
        convert the given string using successive prefix look-ups.
        """
        
        valuestring = ""
        key = keystring
        while key:
            value, key = self.find_prefix(key)
            if not value:
                return (valuestring, key)
            valuestring += value
        return (valuestring, key)
        
        
if __name__ == "__main__":    
    t = Trie()
    t.add("foo", "A")
    t.add("fo", "B")
    t.add("l", "C")
    t.add("o", "D")

    assert t.find("fo") == "B"
    assert t.find("fool") == None

    assert t.find_prefix("fo") == ("B", "")
    assert t.find_prefix("fool") == ("A", "l")

    assert t.convert("fo") == ("B", "")
    assert t.convert("fool") == ("AC", "")
