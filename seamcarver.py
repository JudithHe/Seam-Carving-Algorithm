# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 23:51:48 2014
@author: mandar
"""
import scipy
import numpy as np
from skimage import img_as_float
from skimage import filter
from pylab import *
global q
q = 0


def dual_gradient_energy(img):
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    hR = filter.hsobel(R)
    hG = filter.hsobel(G)
    hB = filter.hsobel(B)

    vR = filter.vsobel(R)
    vG = filter.vsobel(G)
    vB = filter.vsobel(B)

    sumRG = np.add(np.square(hR), np.square(hG))
    x_square = np.add(sumRG, np.square(hB))

    sumRGv = np.add(np.square(vR), np.square(vG))
    y_square = np.add(sumRGv, np.square(vB))

    energy = np.add(x_square, y_square)
    return energy


def find_seam(img, energy):
    minval = 1000
    minIndex = 0
    rows = energy.shape[0]
    columns = energy.shape[1]
    sOfIJ = np.zeros(shape=(rows, columns))  # initializing Si(J)
    np.copyto(sOfIJ, energy)

    for i in range(1, rows):  # building Si(j) top to bottom
        for j in range(1, columns - 1):
            if j == 1:
                sOfIJ[i, j] = sOfIJ[i, j] + \
                    min(sOfIJ[i - 1, j], sOfIJ[i - 1, j + 1])
            elif j == columns - 2:
                sOfIJ[i, j] = sOfIJ[i, j] + \
                    min(sOfIJ[i - 1, j - 1], sOfIJ[i - 1, j])
            else:
                sOfIJ[i, j] = sOfIJ[i, j] + min(sOfIJ[i - 1, j - 1], sOfIJ[i- 1, j], sOfIJ[i - 1, j + 1])

    lastRow = sOfIJ[rows - 1, :]
    for p in range(1, columns - 1):  # taking last row and finding minimum
        if lastRow[p] < minval:
            minval = lastRow[p]
            minIndex = p

    # print lastRow
    return minval, minIndex, sOfIJ
    pass


def plot_seam(img, minIndex, sOfIJ):
    rows = img.shape[0]
    columns = img.shape[1]
    k = minIndex
    sOfIJ[rows - 1, k] = 100
    # backtracking from last row to first row
    for i in range(rows - 1, -1, -1):
        # taking one by one row from img matrix and marking kth position in a
        # row
        img[i, k] = [255, 0, 0]
        if i != 0:
            if k == 1:
                if sOfIJ[i - 1, k + 1] < sOfIJ[i - 1, k]:
                    k = k + 1
            elif k == columns - 2:
                if sOfIJ[i - 1, k - 1] < sOfIJ[i - 1, k]:
                    k = k - 1
            else:
                if sOfIJ[i - 1, k - 1] < sOfIJ[i - 1, k] and sOfIJ[i - 1, k - 1] < sOfIJ[i - 1, k + 1]:
                    k = k - 1
                elif sOfIJ[i - 1, k + 1] < sOfIJ[i - 1, k] and sOfIJ[i - 1, k + 1] < sOfIJ[i - 1, k - 1]:
                    k = k + 1

    return img
    pass


def remove_seam(img, minIndex, sOfIJ):
    rows = img.shape[0]
    columns = img.shape[1]
    removed_matrix = np.zeros(shape=(rows, columns - 1, 3))
    k = minIndex
    # backtracking from last row to first row
    for i in range(rows - 1, -1, -1):
        b = img[i, :, :]  # taking one by one row from img matrix
        # deleting kth position in a row
        removed_matrix[i, :, :] = np.delete(b, k, axis=0)
        if i != 0:
            if k == 1:
                if sOfIJ[i - 1, k + 1] < sOfIJ[i - 1, k]:
                    k = k + 1
            elif k == columns - 2:
                if sOfIJ[i - 1, k - 1] < sOfIJ[i - 1, k]:
                    k = k - 1
            else:
                if sOfIJ[i - 1, k - 1] < sOfIJ[i - 1, k] and sOfIJ[i - 1, k - 1] < sOfIJ[i - 1, k + 1]:
                    k = k - 1
                elif sOfIJ[i - 1, k + 1] < sOfIJ[i - 1, k] and sOfIJ[i - 1, k + 1] < sOfIJ[i - 1, k - 1]:
                    k = k + 1
    return removed_matrix
    pass


def main():
    img = imread('givenImg.png')
    img = img_as_float(img)
    subplot(1, 3, 1)
    imshow(imread('givenImg.png'))
    title('Given')
    figure()
    gray()
    """
    >>>img = imread('givenImg.png')
    >>>img = img_as_float(img)
    >>>energy=dual_gradient_energy(img)
    >>>minval,minIndex,sOfIJ=find_seam(img,energy)
    >>>print minval
    0.488050766739
    """
    for i in range(50):
        energy = dual_gradient_energy(img)
        minval, minIndex, sOfIJ = find_seam(img, energy)
        img = plot_seam(img, minIndex, sOfIJ)
    subplot(1, 3, 2)
    imshow(img)
    title('Seam Plot')
    img = imread('givenImg.png')
    img = img_as_float(img)
    for i in range(50):
        energy = dual_gradient_energy(img)
        minval, minIndex, sOfIJ = find_seam(img, energy)
        print minval
        img = remove_seam(img, minIndex, sOfIJ)
    subplot(1, 3, 3)
    imshow(img)
    title('Resized Image')
    show()
    pass

if __name__ == '__main__':
    main()
