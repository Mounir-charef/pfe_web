from home.dct import *
from home.ap import split, toBinary, CheckFile
import cv2

# LES VARIABLES GLOBAL
QUANT_TABLE = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])
DIMENSIONS = (256, 256)
BLOCK_SIZE = 8


# La function de TATOUAGE
def watermarking(file_name, message):
    # vérifier l'utilisabilité du fichier (taille et type)
    img = CheckFile(file_name)
    # WATERMARK dimensions
    width, height = DIMENSIONS
    leng = len(message)
    # Convertir le msg en une file de 1 et de 0: ['0','1'...]
    msg = split(toBinary(message), 1)

    # rendre les dimensions de l'image compatibles avec des blocs 8x8
    width -= width % 8
    height -= height % 8
    h = height // BLOCK_SIZE
    w = width // BLOCK_SIZE

    # la matrice(array) d'image
    arr = np.array(img)
    nrr = arr.copy()
    # convertir l'image a YCbCr
    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2YCrCb)
    padded_img = np.zeros((height, width), dtype='float32')
    padded_img[0:height, 0:width] = arr[0:height, 0:width, 0]
    for i in range(h):

        row_ind_1 = i * BLOCK_SIZE
        row_ind_2 = row_ind_1 + BLOCK_SIZE

        for j in range(w):
            col_ind_1 = j * BLOCK_SIZE
            col_ind_2 = col_ind_1 + BLOCK_SIZE
            # La block 8x8
            block = padded_img[row_ind_1: row_ind_2, col_ind_1: col_ind_2]
            # applique la dct et la quantization
            block = dct(block)
            block = np.divide(block, QUANT_TABLE)
            block = np.round(block)
            # le Zigzag et l'insertion de message
            zig = np.int16(zigzag(block))
            if msg:
                zig = insert(zig, msg)
            # Applique la inverse dct et la dequantization
            block = inverse_zigzag(zig, 8, 8)
            block = np.multiply(block, QUANT_TABLE)
            block = idct(block)
            block = block.clip(0, 255)
            padded_img[row_ind_1: row_ind_2, col_ind_1: col_ind_2] = block
    # Recuperer l'image RGB et calculer le PSNR et MSE
    for i in range(height):
        for j in range(width):
            arr[i, j, 0] = padded_img[i, j]
    arr = cv2.cvtColor(arr, cv2.COLOR_YCR_CB2RGB)
    img = Image.fromarray(arr, 'RGB')
    psnr, mse = PSNR(nrr, arr)
    return img, psnr, mse, leng


# La function d'extration
def extract(file_name, leng):
    leng *= 8
    img = CheckFile(file_name)
    msg = ''
    width, height = DIMENSIONS
    width -= width % 8
    height -= height % 8
    h = height // BLOCK_SIZE
    w = width // BLOCK_SIZE
    arr = np.array(img)
    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2YCrCb)
    padded_img = np.zeros((height, width), dtype='float32')
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
            block = padded_img[row_ind_1: row_ind_2, col_ind_1: col_ind_2]
            block = dct(block)
            block = np.divide(block, QUANT_TABLE)
            block = np.round(block)
            zig = np.int16(zigzag(block))
            msg += bin(zig[3])[-1]
    msg = [msg[i:i + 8] for i in range(0, len(msg), 8)]  # ['11011001','10111101'...]
    msg = text(msg)
    return msg


# Pour assurer le fichie et traiter comme un bibliothèque
if __name__ == '__main__':
    exit('wrong file excuted')
