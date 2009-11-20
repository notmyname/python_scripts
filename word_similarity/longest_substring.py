#!/usr/bin/env python2.4

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
	    print `chunk`,i,i+j
	    if chunk in two:
		if len(chunk) > len(longest):
		    longest = chunk

    return longest

if __name__ == '__main__':
    #print longest_substring('again and again I coughed repeatedly','repeat: the cat coughs again and again')
    f = open('/dev/random','rb')
    str1 = f.read(1024)
    str2 = f.read(1024)
    f.close()
    print longest_substring(str1,str2)
