total_size_to_write = 16384
chunk_size_to_buffer = 2**20
chunks_to_write = max(total_size_to_write / chunk_size_to_buffer, 1)
chunk = 'x' * min(total_size_to_write, chunk_size_to_buffer)

for i in xrange(1000):
    with open('%d.dat'%i, 'wb') as f:
        for _ in xrange(chunks_to_write):
            f.write(chunk)
