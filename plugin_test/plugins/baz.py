class Another(object):
    def whatever(self):
	print 'blahblah'

class X:
    def Y(self):
	return 'in Y'

x = X()

root = Another()
root.x = x
