#!/usr/bin/env python2.4

from Common import *

dict1 = {'one':1,'two':2}
dict2 = {'three':3,'four':4}
dict3 = {'one':2}
dict4 = {'one':'1'}
dict5 = {'a':dict1}
dict6 = {'a':dict2}
dict7 = {'b':dict5}
dict8 = {'c':dict7}

dicta = {'d':[1,2,3]}
dictb = {'e':[4,5,6]}
dictc = {'d':[4,5,6]}
dictd = {'f':dicta}
dicte = {'f':dictb}
dictf = {'f':dictc}

dictg = {'g':[dict1]}
dicth = {'g':[dict2]}

print deep_update(dict1,dict2)
print deep_update(dict1,dict3)
print deep_update(dict1,dict4)
print deep_update(dict5,dict6)
print deep_update(dict7,dict8)

print deep_update(dicta,dictb)
print deep_update(dicta,dictc)
print deep_update(dictd,dicte)
print deep_update(dictd,dictf)

print deep_update(dictg,dicth)
