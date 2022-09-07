from home.ap import *
import numpy as np
from home.dct import PSNR


def LsbWatermark(filename, name):
    img = CheckFile(filename)
    value = split(toBinary(name))
    leng = len(value)
    width, height = img.size
    pmap = np.array(img)
    arr = pmap.copy()
    for i in range(width):
        for j in range(height):
            if not value:
                break
            msg = value.pop(0)
            r, g, b = pmap[i, j]
            nr = bin(r)[2:-2]
            nr += msg
            nr = int(nr, 2)
            pmap[i, j, 0] = nr
    img = Image.fromarray(pmap)
    psnr, mse = PSNR(arr, pmap)
    return img, leng, psnr, mse


def LsbExtract(filename, leng):
    img = Image.open(filename)
    width, height = img.size
    pmap = np.array(img)
    msg = []
    for i in range(width):
        for j in range(height):
            if not leng:
                break
            leng = leng - 1
            r, g, b = pmap[i, j]
            r = bin(r)[2:]
            if len(r) > 1:
                r = r[-2:]
            else:
                r = '0' + r
            msg.append(r)
    msg = text(merge(msg))
    return msg


if __name__ == '__main__':
    exit('wrong file')
