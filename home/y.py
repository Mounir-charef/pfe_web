from home.dct import *
from home.ap import split, toBinary
import cv2
quantTable = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])


def extract(file_name, leng):
    leng *= 8
    img = Image.open(file_name)
    msg = ''
    width, height = (256,256)
    width -= width % 8
    height -= height % 8
    BLOCK_SIZE = 8
    h = height // BLOCK_SIZE
    w = width // BLOCK_SIZE
    arr = np.array(img)
    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2YCrCb)
    padded_img = np.zeros((height, width), dtype='int16')
    padded_img[0:height, 0:width] = arr[0:height, 0:width, 0]
    for i in range(h):
        row_ind_1 = i * BLOCK_SIZE
        row_ind_2 = row_ind_1 + BLOCK_SIZE

        for j in range(w):
            if not leng:
                break
            leng -= 1
            col_ind_1 = j * BLOCK_SIZE
            col_ind_2 = col_ind_1 + BLOCK_SIZE
            block = padded_img[row_ind_1: row_ind_2, col_ind_1: col_ind_2].astype('float32')
            block -= 128
            block = dct(block)
            block = np.divide(block, quantTable)
            block = np.round(block)
            zig = np.int16(zigzag(block))
            msg += bin(zig[3])[-1]
    msg = [msg[i:i + 8] for i in range(0, len(msg), 8)]
    msg = text(msg)
    print(msg)
    return msg


def watermarking(file_name, message):
    img = Image.open(file_name).convert('RGB')
    msg = message
    leng = len(msg)
    # we need to work on the size
    msg = split(toBinary(msg), 1)
    width, height = (256,256)
    width -= width % 8
    height -= height % 8
    BLOCK_SIZE = 8
    h = height // BLOCK_SIZE
    w = width // BLOCK_SIZE
    arr = np.array(img)
    nrr = arr.copy()
    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2YCrCb)
    padded_img = np.zeros((height, width), dtype='int16')
    padded_img[0:height, 0:width] = arr[0:height, 0:width, 0]
    for i in range(h):

        row_ind_1 = i * BLOCK_SIZE
        row_ind_2 = row_ind_1 + BLOCK_SIZE

        for j in range(w):
            col_ind_1 = j * BLOCK_SIZE
            col_ind_2 = col_ind_1 + BLOCK_SIZE
            block = padded_img[row_ind_1: row_ind_2, col_ind_1: col_ind_2].astype('float32')
            block -= 128
            block = dct(block)
            block = np.divide(block, quantTable)
            block = np.round(block)
            zig = np.int16(zigzag(block))
            if msg:
                zig = insert(zig, msg)
            block = inverse_zigzag(zig, 8, 8)
            block = np.multiply(block, quantTable)
            block = idct(block)
            block += 128
            block = block.clip(0, 255)
            padded_img[row_ind_1: row_ind_2, col_ind_1: col_ind_2] = block
    for i in range(height):
        for j in range(width):
            arr[i, j, 0] = padded_img[i, j]
    arr = cv2.cvtColor(arr, cv2.COLOR_YCR_CB2RGB)
    img = Image.fromarray(arr, 'RGB')
    return img, PSNR(nrr, arr), leng


if __name__ == '__main__':
    exit('wrong file excuted')