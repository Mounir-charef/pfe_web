from PIL import Image
from home.ap import *
import numpy as np
from home.dct import PSNR

def LsbWatermark(filename, name):
    img = Image.open(filename).convert('RGB')
    if(img.size[0]<256 or img.size[1]<256):
        raise Exception("Image too small for watermarking")
    value = split(toBinary(name))
    leng = len(value)
    width, height = img.size
    pmap = np.array(img)
    arr = pmap.copy()
    for i in range(width):
        for j in range(height):
            if (not value):
                break
            msg = value.pop(0)
            r, g, b = pmap[i, j]
            nr = bin(r)[2:-2]
            nr += msg
            nr = int(nr, 2)
            pmap[i, j, 0] = nr
    img = Image.fromarray(pmap)
    psnr, mse = PSNR(arr, pmap)
    print(psnr, mse)
    return img, leng, psnr, mse


def LsbExtract(filename, leng):
    img = Image.open(filename)
    width, height = img.size
    pmap = np.array(img)
    msg = []
    for i in range(width):
        for j in range(height):
            if (leng == 0):
                break
            leng = leng - 1
            r, g, b = pmap[i, j]
            r = bin(r)[2:]
            if (len(r) > 1):
                r = r[-2:]
            else:
                r = '0' + r
            msg.append(r)
    msg = text(merge(msg))
    return msg


if __name__ == '__main__':
    print('wrong file')

