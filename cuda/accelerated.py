#!/usr/bin/env python

import sys
import time

import PIL.Image

import pycuda.driver as cuda
import pycuda.autoinit

import numpy

LINEAR = True

mod = cuda.SourceModule("""
    #define Z_MAX %(z_max)d
    __device__ float calc(float val_a, float val_b, int index)
    {
        /*if (index %% Z_MAX == 0)
            return 0.0;*/
        return val_a * val_b / 256.0;
        //return min(255.0, val_a+val_b);
        //return max(0.0, val_a-val_b);
    }
    __global__ void modify(float *a, float *b, float *c)
    {
        int row_len = gridDim.x*blockDim.x*Z_MAX;
        int block_offset_x = blockDim.x*blockIdx.x*Z_MAX;
        int block_offset_y = blockDim.y*blockIdx.y*row_len;
        int i = threadIdx.x*Z_MAX + threadIdx.y*row_len + threadIdx.z + block_offset_x + block_offset_y;
        if (i > %(max)d)
            return;
        c[i] = calc(a[i], b[i], i);
    }
    __global__ void modify_linear(float *a, float *b, float *c)
    {
        int block_offset_x = blockDim.x*blockIdx.x;
        int i = threadIdx.x + block_offset_x;
        /*if (i > %(max)d)
            return;*/
        c[i] = calc(a[i], b[i], i);
    }
    """ % {'z_max':3, 'max':2896782})#{'z_max':d, 'max':img1_arr.size})
if LINEAR:
    func = mod.get_function("modify_linear")
else:
    func = mod.get_function("modify")

def get_image_data():
    image_data = []
    for i in xrange(50):
        page_num = i + 1
        path1, path2 = 'form1.%d.png'%page_num, 'form2.%d.png'%page_num
        
        img1_arr = load_image(path1)
        img2_arr = load_image(path2)
        
        image_data.append((path1,img1_arr, path2,img2_arr))
    return image_data

def load_image(path):
    img1 = PIL.Image.open('work/%s'%path)
    img1 = img1.convert('RGB')
    img1_arr = numpy.asarray(img1)
    img1_arr = img1_arr.astype(numpy.float32)
    return img1_arr

def save_image(img_data, out_path):
    img3 = PIL.Image.fromarray(img_data)
    img3.save('work/composite_%s'%out_path)

def do_work(work_set, a_gpu, b_gpu, c_gpu, block_size, grid_size):
    final = numpy.empty_like(load_image(work_set[0][0]))
    for path1, path2 in work_set:
        img1_arr = load_image(path1)
        img2_arr = load_image(path2)
        cuda.memcpy_htod(a_gpu, img1_arr)
        cuda.memcpy_htod(b_gpu, img2_arr)
        
        func(a_gpu, b_gpu, c_gpu, block=block_size, grid=grid_size)
        
        final = final.astype(numpy.float32)
        cuda.memcpy_dtoh(final, c_gpu)
        final = final.astype(numpy.uint8)
        
        #save_image(final, (path1+path2).replace('png','') + 'png')

def main():
    (h, w), d = (826,1169), 3 #img1.size, len(img1_arr[0][0])
    if LINEAR:
        thread_x, thread_y, thread_z = 128,1,1
        block_x, block_y = (w*h*d)/thread_x, 1
        if (w*h*d)%thread_x:
            block_x += 1
    else:
        thread_x, thread_y, thread_z = 16, 8, d
        block_x, block_y = h / thread_x, w / thread_y
        if h % thread_x:
            block_x += 1
        if w % thread_y:
            block_y += 1
    #print (h,w,d), (thread_x,thread_y,thread_z), (block_x,block_y)

    image_data_size = 2896782 * 4
    a_gpu = cuda.mem_alloc(image_data_size)
    b_gpu = cuda.mem_alloc(image_data_size)
    c_gpu = cuda.mem_alloc(image_data_size)
    
    image_path_pairs = []
    for i in xrange(50):
        page_num = i + 1
        path1, path2 = 'form1.%d.png'%page_num, 'form2.%d.png'%page_num
        image_path_pairs.append((path1,path2))
    
    do_work(image_path_pairs, a_gpu, b_gpu, c_gpu, (thread_x, thread_y, thread_z), (block_x, block_y))

if __name__ == '__main__':
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
