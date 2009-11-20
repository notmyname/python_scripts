print "init"

import time
import threading

class kkc (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__ (self)
        self.__running = True
        self.start ()
        
    def terminate (self):
        self.__running = False
        self.join ()
        
    def run (self):
        while self.__running:
            print "parsing time..."
            time.strptime ("2007-11-10 15-41-30", "%Y-%m-%d %H-%M-%S")
            print "...done"
            time.sleep (1.0)

kk = kkc ()
print "started"

try:
    while True:
        time.sleep (1.0)
except:
    pass

print "finishing"
kk.terminate ()

print "done"
