import numpy as np
import matplotlib.pyplot as plt
from PIL.Image import *
from scipy import ndimage

def imap1(im):
    print('testing the picture . . .')
    a = Image.getpixel(im, (0, 0))
    if type(a) == int:
        return im
    else:
        c, l = im.size
        imarr = np.asarray(im)
        neim = np.zeros((l, c))
        for i in range(l):
            for j in range(c):
                t = imarr[i, j]
                ts = sum(t)/len(t)
                neim[i, j] = ts
        return neim

def Harris(im):
    neim = imap1(im)
    imarr = np.asarray(neim, dtype=np.float64)
    ix = ndimage.sobel(imarr, 0)
    iy = ndimage.sobel(imarr, 1)
    ix2 = ix * ix
    iy2 = iy * iy
    ixy = ix * iy
    ix2 = ndimage.gaussian_filter(ix2, sigma=2)
    iy2 = ndimage.gaussian_filter(iy2, sigma=2)
    ixy = ndimage.gaussian_filter(ixy, sigma=2)
    c, l = imarr.shape
    result = np.zeros((c, l))
    r = np.zeros((c, l))
    rmax = 0
    for i in range(c):
        print('loking for corner . . .')
        for j in range(l):
            print('test ',j)
            m = np.array([[ix2[i, j], ixy[i, j]], [ixy[i, j], iy2[i, j]]], dtype=np.float64)
            r[i, j] = np.linalg.det(m) - 0.04 * (np.power(np.trace(m), 2))
            if r[i, j] > rmax:
                rmax = r[i, j]
    for i in range(c - 1):
        print(". .")
        for j in range(l - 1):
            print('loking')
            if r[i, j] > 0.01 * rmax and r[i, j] > r[i-1, j-1] and r[i, j] > r[i-1, j+1]\
                                     and r[i, j] > r[i+1, j-1] and r[i, j] > r[i+1, j+1]:
                result[i, j] = 1

    pc, pr = np.where(result == 1)
    plt.plot(pr, pc, 'r+')
    plt.savefig('harris_test.png')
    plt.imshow(im, 'gray')
    plt.show()
    # plt.imsave('harris_test.png', im, 'gray')

im = open('chess.png')
Harris(im)