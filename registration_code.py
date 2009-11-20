#!/usr/bin/env python2.4

# generates and verifies a sequence of digits
# uses the same method that is used for most bar codes

import random

def find_check(code):
    if len(code) % 2:
        even = [code[i] for i in range(0,len(code)+1,2)]
        odd = [code[i] for i in range(1,len(code),2)]
    else:
        even = [code[i] for i in range(0,len(code),2)]
        odd = [code[i] for i in range(1,len(code)+1,2)]

    even_sum = sum(int(i) for i in even)
    odd_sum = sum(int(i) for i in odd)
    total = even_sum + (3 * odd_sum)

    check = 10 - (total % 10)
    if check == 10: check = 0
    return check

def check_code(code):
    return find_check(code[:-1]) == int(code[-1])

def generate_code(length=9):
    new_code = []
    for i in range(length-1):
        new_code.append(str(random.randrange(0,10)))

    new_code = ''.join(new_code)
    check = find_check(new_code)
    new_code += str(check)
    return new_code
    
for i in range(10):
    code = generate_code(25)
    print code,check_code(code)
