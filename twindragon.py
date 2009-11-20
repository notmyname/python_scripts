#!/usr/bin/env python
def create_twindragon(n):
    """calculate the dragon set, according to Knuth"""
    s = set([0.0+0.0j])
    for i in range(n):
        new_power = (1.0-1.0j)**(-i)
        s |= set(x+new_power for x in s)
    return s

if __name__ == '__main__':
    import sys
    print create_twindragon(int(sys.argv[1]))
