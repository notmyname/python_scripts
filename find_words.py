import sys

letters = ''.join(sys.argv[1].split()).lower()

words = [x.strip() for x in open('/usr/share/dict/words','rb').readlines()]

letters_len = len(letters)
i = 0
while i < letters_len:
    for j in xrange(letters_len, i, -1):
        snip = letters[i:j]
        if snip in words:
            print snip,
            break
    i = j
