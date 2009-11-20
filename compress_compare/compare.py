#!/usr/bin/python2.5

import PIL.Image
import PIL.ImageColor
import numpy
import sys

image1 = numpy.load('form1.1.npy').tolist()
image2 = numpy.load('form2.1.npy').tolist()

#image1 = [4,4,1,6,2,3,0,2,3]
#image2 = [4,4,1,3,7,2,4]

w1 = image1.pop(0)
h1 = image1.pop(0)
color1 = image1.pop(0)
w2 = image2.pop(0)
h2 = image2.pop(0)
color2 = image2.pop(0)

assert h1==h2 and w1==w2

final = numpy.zeros(h1*w1, numpy.uint8)

start_color = color1
if color2 != start_color:
    image2.insert(start_color,0)

x = y = 0
black = (0,0,0,255)
black_index = 0

white = (255,255,255,255)
white_index = 1

diff_color = (127,0,0,255)
diff_color_index = 2

image_count = 2

color_palette = numpy.array([black, white]+[diff_color]*image_count, numpy.uint8)

dtheta = 360.0 / image_count
for i in xrange(image_count):
    theta = dtheta * i
    c = PIL.ImageColor.getcolor("hsl(%3.0f,100%%,35%%)" % theta, "RGBA")
    color_palette[i+2] = c

if 0:
    def uncompress(start_color, image):
        color = start_color
        ret = []
        for run in image:
            ret.extend([color]*run)
            color = not color
        return ret

    print 'uncompress'
    raw1 = numpy.array(uncompress(color1, image1), numpy.uint8) * 2
    raw2 = numpy.array(uncompress(color2, image2), numpy.uint8) * 3
    print 'make diff'
    diff = ((raw1 ^ raw2)) #| (raw1 & raw2)
    print 'color image'
    colored = color_palette[diff]
    print 'reshape'
    colored.shape = (h1,w1,4)
    print 'make image and save'
    out = PIL.Image.fromarray(colored, 'RGBA') # NOTE: there was a bug in PIL.Image.fromarray that had to be patched
    out.save('out.png')

    sys.exit(1)

# index to keep track of where in the final image we currently are
final_x = 0

# start with the opposite color (the first time through we toggle the color)
if start_color == 1:
    color_index = black_index
else:
    color_index = white_index

while image1 or image2:
    skip = False
    try:
        new_x = image1.pop(0)
    except:
        new_x = 0
    else:
        try:
            while new_x == 0:
                skip = True
                new_x = image1.pop(0)
        except:
            new_x = 0
    try:
        new_y = image2.pop(0)
    except:
        new_y = 0
    else:
        try:
            while new_y == 0:
                skip = True
                new_y = image2.pop(0)
        except:
            new_y = 0
    x += new_x
    y += new_y
    min_run = min(x, y)
    x -= min_run
    y -= min_run
    if not skip and min_run > 0:
        if color_index == white_index:
            color_index = black_index
        else:
            color_index = white_index
        #print 'a',final_x,final_x+min_run, min_run
        final[final_x:final_x+min_run] = color_index
        final_x += min_run
    if x > 0:
        diff = x
    else:
        diff = y
    if diff > 0:
        #print 'b',final_x,final_x+diff, diff
        final[final_x:final_x+diff] = diff_color_index
        final_x += diff
        x -= diff
        y -= diff


print 'making array'
arr = color_palette[final]

print 'making image'
arr.shape = (h1,w1,4)
out = PIL.Image.fromarray(arr, 'RGBA') # NOTE: there was a bug in PIL.Image.fromarray that had to be patched
out.save('out.png')
