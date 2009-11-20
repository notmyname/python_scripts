import socket
import sys
import time

printer_ip = '200.200.60.35'
port = 9100

msg = 'Ready'

_max_line_len = 20

try:
    printer_ip = sys.argv[1]
    msg = sys.argv[2]
except:
    print 'Usage: %s printer_ip message'
else:
    words = msg.split()
    lines = [['Ready               '],[],[],[]]
    current_line = 1
    for word in words:
        len_word = len(word)
        line_len = sum(len(x) for x in lines[current_line]) + len(lines[current_line]) - 1
        if line_len + len_word + 1 > _max_line_len:
            if _max_line_len-line_len-1 >= 0:
                lines[current_line].append(' '*(_max_line_len-line_len-1))
            current_line += 1
            if current_line >= 4:
                break
            lines[current_line] = [word]
        else:
            lines[current_line].append(word)
    msg = ''.join(' '.join(y for y in x) for x in lines)
    print `msg[:_max_line_len]`
    print `msg[_max_line_len:_max_line_len*2]`
    print `msg[_max_line_len*2:_max_line_len*3]`
    print `msg[_max_line_len*3:_max_line_len*4]`
    
    command = '\033%%-12345X@PJL RDYMSG DISPLAY = "%s"\r\n\033%%-12345X\r\n' % msg[:_max_line_len*4]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((printer_ip,port))
    s.send(command)
    s.close()
