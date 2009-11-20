#!/usr/bin/env python2.5

import re, string, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

# this should be some collection of words (like a story) so frequency can be established
# a dictionary listing of words will not be able to give good suggestions for corrections
#NWORDS = train(words(file('/usr1/hcsjad/words/new_words').read()))
NWORDS = train(words(file('/home/john/test_speach').read()))

def edits1(word):
    n = len(word)
    return set([word[0:i]+word[i+1:] for i in range(n)] + ## deletion
               [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] + ## transposition
               [word[0:i]+c+word[i+1:] for i in range(n) for c in string.lowercase] + ## alteration
               [word[0:i]+c+word[i:] for i in range(n+1) for c in string.lowercase]) ## insertion

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    return max(known([word]) or known(edits1(word)) or known_edits2(word) or [word],
               key=lambda w: NWORDS[w])

if __name__ == '__main__':
    import sys
    for arg in sys.argv[1:]:
        print '%s: %s' % (arg, correct(arg))
