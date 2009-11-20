# Author: John Dickinson

import time
import os

import PIL.Image
import pycuda.driver as cuda
import pycuda.autoinit
import numpy

GPU = cuda.Device(0)
GPU_ATTRIBUTES = dict((str(att), value) for att, value in GPU.get_attributes().iteritems())

def get_cuda_func(z_max, max_arr_size, total_image_count):
    raw = open('/home/john/python_scripts/cuda/cuda_code.c', 'rb').read()
    processed = raw % {'z_max':z_max, 'max':max_arr_size, 'total_image_count':total_image_count}
    mod = cuda.SourceModule(processed)
    return mod.get_function("modify")

def load_img_arr(img_path):
    if not img_path.endswith('.npy'):
        img1 = PIL.Image.open(img_path)
        img1_arr = numpy.asarray(img1)
        return img1_arr, 'RGBA'#img1.mode
        img_path = os.path.splitext(img_path)[0]+'.npy'
        numpy.save(img_path, img1_arr)
    img1_arr = numpy.load(img_path)
    return img1_arr, 'RGBA'#img1.mode

def save_image_arr(img_arr, mode, out_path):
    #numpy.save(out_path, img_arr)
    #return
    img = PIL.Image.fromarray(img_arr, mode)
    img.save(out_path+'.png')

def merge_images(image1, image2):
    thread_x, thread_y, thread_z = GPU_ATTRIBUTES['MAX_THREADS_PER_BLOCK']/GPU_ATTRIBUTES['MULTIPROCESSOR_COUNT'], 1, 1
    block_size = (thread_x, thread_y, thread_z)
    i1 = numpy.asarray(image1)
    h, w, d = len(i1), len(i1[0]), len(i1[0][0])
    block_x, block_y = i1.size/d/thread_x, 1
    if (i1.size/d) % thread_x:
        block_x += 1
    grid_size = (block_x, block_y)
    func = get_cuda_func(d, i1.size, 2)
    a_gpu = cuda.mem_alloc(i1.size)
    b_gpu = cuda.mem_alloc(i1.size)
    cuda.memcpy_htod(a_gpu, i1)
    i2 = numpy.asarray(image2)
    cuda.memcpy_htod(b_gpu, i2)
    func(a_gpu, b_gpu, numpy.uint16(1), block=block_size, grid=grid_size)
    final = numpy.empty_like(i1)
    cuda.memcpy_dtoh(final, a_gpu)
    return PIL.Image.fromarray(final, image1.mode)

def merge(image_groups, out_name_template='work/test_out.%d', callback=None):
    ret = []
    
    thread_x, thread_y, thread_z = GPU_ATTRIBUTES['MAX_THREADS_PER_BLOCK']/GPU_ATTRIBUTES['MULTIPROCESSOR_COUNT'], 1, 1
    block_size = (thread_x, thread_y, thread_z)
    
    # arr       <- all rows
    # arr[0]    <- pixels in first row
    # arr[0][0] <- first pixel in first row (RGB[A])
    
    # load the first one to precompute values
    total_image_count = len(image_groups[0])
    i1, mode1 = load_img_arr(image_groups[0][0])
    blank = numpy.empty_like(i1)
    #blank = numpy.ones(i1.shape)*255
    blank = blank.astype(numpy.uint8)
    h, w, d = len(i1), len(i1[0]), len(i1[0][0])
    block_x, block_y = i1.size/d/thread_x, 1
    if (i1.size/d) % thread_x:
        block_x += 1
    grid_size = (block_x, block_y)
    func = get_cuda_func(d, i1.size, total_image_count)
    
    for i, group in enumerate(image_groups):
        a_gpu = cuda.mem_alloc(i1.size)
        b_gpu = cuda.mem_alloc(i1.size)
        cuda.memcpy_htod(a_gpu, blank)
        for j, image_path in enumerate(group):
            i2 = load_img_arr(image_path)[0]
            cuda.memcpy_htod(b_gpu, i2)
            t = func(a_gpu, b_gpu, numpy.uint16(j), block=block_size, grid=grid_size, time_kernel=True)
            print t
        final = numpy.empty_like(blank)
        cuda.memcpy_dtoh(final, a_gpu)
        
        out_name = out_name_template%(i+1)
        save_image_arr(final, mode1, out_name)
        ret.append(out_name)
        
        # free memory on the gpu
        del a_gpu
        del b_gpu
    return ret

def main():
    image_groups = []
    for i in xrange(1,25):
        group = []
        group.append('work/form1.%d.npy'%i)
        group.append('work/form2.%d.npy'%i)
        group.append('work/form3.%d.npy'%i)
        #group.append('ian1.npy')
        #group.append('ian2.npy')
        image_groups.append(group)
    
    merge(image_groups)
    print 'done merging %d total images' % (len(image_groups) * len(image_groups[0]))

if __name__ == '__main__':
    import sys
    if '--profile' in sys.argv:
        import cProfile
        import pstats
        import os
        
        cProfile.run('main()', '/tmp/profile.stats')
        s = pstats.Stats('/tmp/profile.stats')
        s.sort_stats('time')
        s.print_stats(20)
        os.remove('/tmp/profile.stats')
    else:
        main()
