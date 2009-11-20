#!/usr/bin/python2.5

import PIL.Image
import numpy
import sys
sys.path.insert(0,'/home/john/python_scripts')
import stats

def compress(image):
    compressed_arr = []
    for row in arr:
        dest_row = []
        for col in row:
            color = tuple(col[:3]) # ignore alpha
            if color == (0, 0, 0):
                color = 0
            elif color == (255, 255, 255):
                color = 1
            else:
                print 'unsupported color'
            dest_row.append(color)
        compressed_arr.append(dest_row)

    current_color = compressed_arr[0][0]
    encoded_arr = list(image.size) + [current_color]
    run = 0
    for row in compressed_arr:
        for point in row:
            if point == current_color and (run+1) < 2**16:
                run += 1
            else:
                encoded_arr.append(run)
                if (run+1) >= 2**16:
                    encoded_arr.append(0) # run of 0 to keep toggle rule working
                current_color = point
                run = 1
    encoded_arr.append(run)

    return numpy.asarray(encoded_arr).astype(numpy.uint16)

image = PIL.Image.open('form1.1.png')
arr = numpy.asarray(image)
print arr.size, arr.shape

encoded_arr = compress(image)

print encoded_arr.size, encoded_arr.shape, encoded_arr.dtype
print encoded_arr
numpy.save('form1.1', encoded_arr)
print stats.stats(encoded_arr.tolist()[1:])

image = PIL.Image.open('form2.1.png')
arr = numpy.asarray(image)
print arr.size, arr.shape

encoded_arr = compress(image)

print encoded_arr.size, encoded_arr.shape, encoded_arr.dtype
print encoded_arr
numpy.save('form2.1', encoded_arr)
print stats.stats(encoded_arr.tolist()[1:])
