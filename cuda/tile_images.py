# Author: John Dickinson

import time

import PIL.Image
import pycuda.driver as cuda
import pycuda.autoinit
import numpy

GPU = cuda.Device(0)
GPU_ATTRIBUTES = dict((str(att), value) for att, value in GPU.get_attributes().iteritems())

def load_img_arr(img_path):
    if not img_path.endswith('.npy'):
        img1 = PIL.Image.open(img_path)
        img1_arr = numpy.asarray(img1)
        img_path = os.path.splitext(img_path)[0]+'.npy'
        numpy.save(img_path, img1_arr)
    img1_arr = numpy.load(img_path)
    return img1_arr

def save_image_arr(img_arr, mode, out_path):
    img = PIL.Image.fromarray(img_arr, mode)
    img.save(out_path)

def main():
    arr, mode1 = load_img_arr('work/form1.1.npy')
    image_data_size = arr.size
    thread_x, thread_y, thread_z = GPU_ATTRIBUTES['MAX_THREADS_PER_BLOCK']/GPU_ATTRIBUTES['MULTIPROCESSOR_COUNT'], 1, 1
    block_size = (thread_x, thread_y, thread_z)
    
    # arr       <- all rows
    # arr[0]    <- pixels in first row
    # arr[0][0] <- first pixel in first row (RGB[A])
    
    #TODO:
    # make a strip of images up to max images, max grid dim, or max image count
    # if there are images left over, start making another strip (same conditions as above)
    # if we finished a whole strip, add the strip to the existing strips
    # repeat until all images are used up or we have more strips than that grid dim
    
    pairs_processed = 0
    total_image_pairs = 50
    while pairs_processed < total_image_pairs:
        free_memory = cuda.mem_get_info()[0]
        half_memory = free_memory / 2
        max_group_count = (half_memory / image_data_size) # number of image pairs that can be loaded
        y_strip_count = 0
        group_count = 0
        strip1 = numpy.Array()
        strip2 = numpy.Array()
        while group_count < max_group_count and y_strip_count < GPU_ATTRIBUTES['MAX_GRID_DIM_Y']:
            i1 = load_img_arr('work/form1.%d.npy' % (pairs_processed+1))
            i2 = load_img_arr('work/form2.%d.npy' % (pairs_processed+1))
            group_count += 1
            pairs_processed += 1
            x_strip_count = 0
            # make strip here
    
    
    
    
    
    
    
    
    images_processed = 0
    image_count = 50
    block_y = 1
    while images_processed < image_count:
        free_memory = cuda.mem_get_info()[0]
        half_memory = free_memory / 2
        image_group_count = (half_memory / image_data_size) - 1 # number of image pairs that can be loaded
        
        block1 = load_img_arr('work/form1.%d.npy'%(images_processed+1))[0]
        block2 = load_img_arr('work/form2.%d.npy'%(images_processed+1))[0]
        count = 1
        for i in xrange(images_processed+1, images_processed+image_group_count):
            if i > image_count:
                break
            
            i1 = load_img_arr('work/form1.%d.npy'%i)[0]
            i2 = load_img_arr('work/form2.%d.npy'%i)[0]
            
            h, w, d = len(block1), len(block1[0]), len(block1[0][0])
            new_block_x = (block1.size + i1.size) / thread_x
            if (block1.size + i1.size) % thread_x:
                new_block_x += 1
            new_block_y = block_y
            if new_block_x > GPU_ATTRIBUTES['MAX_GRID_DIM_X']:
                new_block_y += 1
                if new_block_y > GPU_ATTRIBUTES['MAX_GRID_DIM_Y']:
                    raise Exception('Grid getting too big')
                block1 = numpy.concatenate((block1,i1), axis=1)
                block2 = numpy.concatenate((block2,i2), axis=1)
                block_y = new_block_y
            else:
                block1 = numpy.concatenate((block1,i1), axis=0)
                block2 = numpy.concatenate((block2,i2), axis=0)
                block_x = new_block_x
            count += 1
        
        grid_size = (block_x, block_y)
        print grid_size
        
        save_image_arr(block1, mode1, 'grid_out.%d.png' % images_processed)
        
        images_processed += image_group_count

if __name__ == '__main__':
    import sys
    if '--profile' in sys.argv:
        import cProfile
        import pstats
        import os
        
        cProfile.run('main()', '/tmp/profile.stats')
        s = pstats.Stats('/tmp/profile.stats')
        s.sort_stats('cumulative')
        s.print_stats(20)
        os.remove('/tmp/profile.stats')
    else:
        main()
