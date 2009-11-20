#!/usr/bin/env python2.4

from Common import infix,Infix

#using decorator method

@infix
def foo(left,right):
    return left+right

print foo(1,2)
print 1 <<foo>> 2
print "a" |foo| "b"
print 2 <<foo>> 5

print

#not using decorator

def bar(left,right):
    return left+right
baz = Infix(bar) # this line does the same thing as the decorator above

print bar(1,2)
print baz(1,2)
print "a" |baz| "b"
print 2 <<baz>> 5
print 2 >>baz<< 5

print

# more fun

@infix
def istwice(left,right):
    return (right*2)==left

print 4 |istwice| 2
print 2 |istwice| 4
print 2 <<istwice>> 4

print


class klass(object):
    def __init__(self,v):
        self._value = v
    def value(self):
        return self._value

@infix
def has_same_value_as(left,right):
    return left.value() == right.value()

k1 = klass(1)
k2 = klass(2)
k3 = klass(1)

print has_same_value_as(k1,k2)
print k1 <<has_same_value_as>> k2
print k1 <<has_same_value_as>> k3

print


class person(object):
    def __init__(self,name,last):
        self.name = name
        self.last = last
    def __repr__(self):
        return self.name+' '+self.last

@infix
def marry(p1,p2):
    new_last = p1.last
    return p1,person(p2.name,new_last)

@infix
def procreate(p1,p2):
    new_name = p1.name+p2.name
    new_last = p1.last
    if p1.last != p2.last:
        new_last = new_last+'-'+p2.last
    return person(new_name,new_last)

joe = person('joe','smith')
sue = person('sue','jones')

print joe
print sue
betty = joe <<procreate>> sue
print betty
joe,sue = joe <<marry>> sue
print joe
print sue

bobby = procreate(joe,sue)
print bobby
suzy = joe <<procreate>> sue
print suzy
