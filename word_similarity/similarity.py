#!/usr/bin/env python

def longest_substring(one,two):
    lone = len(one)
    ltwo = len(two)

    max_len = min(lone,ltwo)

    longest = ''

    for i in reversed(xrange(max_len)):
	for j in reversed(xrange(i,lone+1-i)):
	    chunk = one[i:i+j]
	    if len(chunk) < len(longest):
		continue
	    if chunk in two:
		if len(chunk) > len(longest):
		    longest = chunk

    return longest

def similar(word1,word2, fast=False):
    if word1 == word2:
	return 1.0

    if fast:
	guess = float(len(word1))/float(len(word2))
	guess = min(float(len(word2))/float(len(word1)),guess)
	if guess < 0.8:
	    return 0.0

    max_len = max(len(word1),len(word2))

    piece1 = longest_substring(word1,word2)

    total_len = len(piece1)

    if piece1 != word1 and piece1 != word2:
	if piece1:
	    word2 = word2.replace(piece1,'')
	    leftover = word1.split(piece1)
	    for piece2 in leftover:
		piece3 = longest_substring(piece2,word2)
		total_len += len(piece3)
		word2 = word2.replace(piece3,'')
    else:
	piece2 = ''
	s2 = 0.0
    
    s1 = float(total_len)/float(max_len)
    return s1

    piece2 = longest_substring(word2,word1)
    s2 = float(len(piece2)/float(max_len))

    return max(s1,s2)

def test(a,b):
    print '%s vs %s'%(a,b), similar(a,b)

def dict_test(word):
    f = open('/usr1/hcsjad/words/new_words','rb')
    for word in f:
	word = word.replace('\n','')
	yield (similar(word1.lower(),word.lower(),True),word)
    f.close()

if __name__ == '__main__':
    test('dog','cot')
    test('me','you')
    test('you','me')
    test('cat','cat')
    test('sudden','suddenly')
    test('suddenly','sudden')
    test('male','female')
    test('female','male')
    test('graduation','gratuation')
    test('a1b2c3','123abc')
    test('test','west')

    word1 = raw_input('word: ')
    print 'Similar words are:'
    results = dict_test(word1)
    for x in reversed(sorted(results)[-25:]):
	print x[1], '(%.2f%%)' % (x[0]*100)
