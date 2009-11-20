#define Z_MAX %(z_max)d
#define TOTAL_IMAGE_COUNT %(total_image_count)d
#define COLOR_MAX 255

__device__ void RGBtoHSV( float, float, float, float *, float *, float * );
__device__ void HSVtoRGB( float *, float *, float *, float, float, float );
__device__ void calc(unsigned char *, unsigned char *, int, unsigned int, unsigned char *);

__global__ void modify(unsigned char *a, unsigned char *b, unsigned int count)
{
    int block_offset_x = blockDim.x*blockIdx.x*Z_MAX;
    long i = threadIdx.x*Z_MAX + block_offset_x;
    unsigned char values[Z_MAX];
    
    calc(a, b, i, count, values);
    for(int j=0; j<Z_MAX; j++)
        a[i+j] = values[j];
}

__device__ void calc(unsigned char *a, unsigned char *b, int index, unsigned int count, unsigned char *result)
{
    int r1,g1,b1;
    int r2,g2,b2;
    
    r1 = a[index];
    g1 = a[index+1];
    b1 = a[index+2];

#if Z_MAX > 3
        int a1;
        a1 = a[index+3];
        if (a1 == 0)
            r1 = g1 = b1 = COLOR_MAX;
#endif
    
    r2 = b[index];
    g2 = b[index+1];
    b2 = b[index+2];
    
#if Z_MAX > 3
        int a2;
        a2 = b[index+3];
        if (a2 == 0)
            r2 = g2 = b2 = COLOR_MAX;
#endif
    
    /*
    float h2,s2,v2;
    float offset_angle = 360.0 / TOTAL_IMAGE_COUNT;
    r2 = (float)b[index]   / COLOR_MAX;
    g2 = (float)b[index+1] / COLOR_MAX;
    b2 = (float)b[index+2] / COLOR_MAX;
    RGBtoHSV(r2,g2,b2, &h2,&s2,&v2);
    h2 += offset_angle*(count);
    while(h2 >= 360.0)
        h2 -= 360.0;
    if(b[index+3] > 0)
    {
        s2 = 1.0;
        v2 = 1.0;
    }
    HSVtoRGB(&r2,&g2,&b2, h2,s2,v2);
    r2 *= COLOR_MAX;
    g2 *= COLOR_MAX;
    b2 *= COLOR_MAX;
    */
    
    result[0] = r1 * r2 / COLOR_MAX;
    result[1] = g1 * g2 / COLOR_MAX;
    result[2] = b1 * b2 / COLOR_MAX;
    
    //result[0] = min(r1 + r2, (float)COLOR_MAX);
    //result[1] = min(g1 + g2, (float)COLOR_MAX);
    //result[2] = min(b1 + b2, (float)COLOR_MAX);
    
    //result[0] = max(r1 - r2, 0.0);
    //result[1] = max(g1 - g2, 0.0);
    //result[2] = max(b1 - b2, 0.0);
    
#if Z_MAX > 3
        // set the alpha chanel
        result[3] = COLOR_MAX; //a[index+3] * b[index+3] / COLOR_MAX;
#endif
}

// r,g,b values are from 0 to 1
// h = [0,360], s = [0,1], v = [0,1]
//        if s == 0, then h = -1 (undefined)

__device__ void RGBtoHSV( float r, float g, float b, float *h, float *s, float *v )
{
    float min_val, max_val, delta;

    min_val = min( r, min(g, b) );
    max_val = max( r, max(g, b) );
    *v = max_val;                // v

    delta = max_val - min_val;

    if( max_val != 0 )
        *s = delta / max_val;        // s
    else {
        // r = g = b = 0        // s = 0, v is undefined
        *s = 0;
        *h = -1;
        return;
    }

    if( r == max_val )
        *h = ( g - b ) / delta;        // between yellow & magenta
    else if( g == max_val )
        *h = 2 + ( b - r ) / delta;    // between cyan & yellow
    else
        *h = 4 + ( r - g ) / delta;    // between magenta & cyan

    *h *= 60;                // degrees
    if( *h < 0 )
        *h += 360;

}

__device__ void HSVtoRGB( float *r, float *g, float *b, float h, float s, float v )
{
    int i;
    float f, p, q, t;

    if( s == 0 ) {
        // achromatic (grey)
        *r = *g = *b = v;
        return;
    }

    h /= 60;            // sector 0 to 5
    i = floor( h );
    f = h - i;            // factorial part of h
    p = v * ( 1 - s );
    q = v * ( 1 - s * f );
    t = v * ( 1 - s * ( 1 - f ) );

    switch( i ) {
        case 0:
            *r = v;
            *g = t;
            *b = p;
            break;
        case 1:
            *r = q;
            *g = v;
            *b = p;
            break;
        case 2:
            *r = p;
            *g = v;
            *b = t;
            break;
        case 3:
            *r = p;
            *g = q;
            *b = v;
            break;
        case 4:
            *r = t;
            *g = p;
            *b = v;
            break;
        default:        // case 5:
            *r = v;
            *g = p;
            *b = q;
            break;
    }

}
