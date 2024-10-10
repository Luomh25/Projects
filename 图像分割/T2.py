import cv2
import numpy as np
import pywt

def jaccard_index(img1, img2):
    intersection = np.logical_and(img1, img2)
    union = np.logical_or(img1, img2)
    jaccard_index = np.sum(intersection) / np.sum(union)
    return jaccard_index

def dice_coefficient(img1, img2):
    intersection = np.sum(img1 / 255 * img2 / 255)
    dice_coefficient = (2. * intersection) / (np.sum(img1 / 255) + np.sum(img2 / 255))
    return dice_coefficient

# img2
# 读取图像
img2 = cv2.imread('Image2.png')
seg2 = cv2.imread('Seg2.png')

# 将图像转换为灰度图像
gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
gray_seg2 = cv2.cvtColor(seg2, cv2.COLOR_BGR2GRAY)

# 应用阈值
ret_img2, thresh_img2 = cv2.threshold(gray_img2, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
ret_seg2, thresh_seg2 = cv2.threshold(gray_seg2, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# 显示结果
cv2.imshow('image2', img2)
cv2.imshow('seg2', seg2)
cv2.imshow('thresh_img2', thresh_img2)
cv2.imshow('thresh_seg2', thresh_seg2)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image2")
Jaccard_index_2 = jaccard_index(thresh_img2, thresh_seg2)
print("Jaccard指数为：", Jaccard_index_2)
Dice_index_2 = dice_coefficient(thresh_img2, thresh_seg2)
print("Dice指数为：", Dice_index_2)

# 进行小波变换
coeffs2 = pywt.dwt2(thresh_img2, 'haar')
cA, (cH, cV, cD) = coeffs2

# 对低频分量进行阈值处理
cA = cv2.convertScaleAbs(cA)
ret, cA = cv2.threshold(cA, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# 进行小波反变换
coeffs2 = cA, (cH, cV, cD)
denoised2 = pywt.idwt2(coeffs2, 'haar')

cv2.imshow('thresh_img1', denoised2)
cv2.imshow('thresh_seg1', thresh_seg2)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image1")
Jaccard_index_2 = jaccard_index(denoised2, thresh_seg2)
print("Jaccard指数为：", Jaccard_index_2)
Dice_index_2 = dice_coefficient(denoised2, thresh_seg2)
print("Dice指数为：", Dice_index_2)
