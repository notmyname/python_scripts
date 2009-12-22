import uuid

for i in xrange(1000):
    f = open('%d.dat'%i, 'wb')
    f.write(uuid.uuid4().hex * 512)
    f.close()