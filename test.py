import numpy as np
import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', action="store", dest="path",
                    help="folder with images", required=True)
args = parser.parse_args()

path = args.path


def pHash(img):
    img64 = np.array(img.convert('L').resize([32, 32]))
    img_dct = dct(img64)
    imgres = [[0 for i in range(8)] for j in range(8)]

    avg = 0.0
    for i in range(len(img_dct)):
        for j in range(len(img_dct[0])):
            avg += img_dct[i][j]
    avg /= 64
    for i in range(len(img_dct)):
        for j in range(len(img_dct[0])):
            imgres[i][j] = int(img_dct[i][j] > avg)
    array1d = np.array(imgres).ravel()

    res = "".join(str(x) for x in array1d)
    return res


def heming(hex1, hex2):
    length = 0
    for i in range(len(hex1)):
        length += int(hex1[i] != hex2[i])
    return length


def dct(A):
    M = len(A)
    B = [[0 for i in range(8)] for j in range(8)]
    a1 = 1.0 / np.sqrt(M)
    a2 = np.sqrt(2.0 / M)
    div = np.pi /(2 * M)

    for p in range(8):
        for q in range(8):
            ss = 0.0
            for m in range(M):
                for n in range(M):
                    ss += A[m][n] * np.cos(p * (2 * m + 1) * div) * np.cos(q * (2 * n + 1) * div)

            A1 = a1 if p == 0 else a2
            A2 = a1 if q == 0 else a2

            B[p][q] = int(A1 * A2 * ss)
    return B


try:
    imgs_names = os.listdir(path)
    hashes = [pHash(Image.open(os.path.join(path, i))) for i in imgs_names]

    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            diff = heming(hashes[i], hashes[j])
            if diff == 0:
                print(imgs_names[i], imgs_names[j], " -- duplicated")
            elif diff <= 5:
                print(imgs_names[i], imgs_names[j], " -- modified")
            elif diff <= 13:
                print(imgs_names[i], imgs_names[j], " -- similar")
except FileNotFoundError:
    print("error: folder not found")
    exit()
