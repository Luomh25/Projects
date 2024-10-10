import cv2
import numpy as np

def jaccard_index(img1, img2):
    intersection = np.logical_and(img1, img2)
    union = np.logical_or(img1, img2)
    jaccard_index = np.sum(intersection) / np.sum(union)
    return jaccard_index

def dice_coefficient(img1, img2):
    intersection = np.sum(img1 / 255 * img2 / 255)
    dice_coefficient = (2. * intersection) / (np.sum(img1 / 255) + np.sum(img2 / 255))
    return dice_coefficient

# img4
# 读取图像
img4 = cv2.imread('Image4.png')
seg4 = cv2.imread('Seg4.png')

# 将图像转换为灰度图像
gray_img4 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
gray_seg4 = cv2.cvtColor(seg4, cv2.COLOR_BGR2GRAY)

# 应用阈值
ret_img4, thresh_img4 = cv2.threshold(gray_img4, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
ret_seg4, thresh_seg4 = cv2.threshold(gray_seg4, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# 显示结果
cv2.imshow('image4', img4)
cv2.imshow('seg4', seg4)
cv2.imshow('thresh_img4', thresh_img4)
cv2.imshow('thresh_seg4', thresh_seg4)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image4")
Jaccard_index_4 = jaccard_index(thresh_img4, thresh_seg4)
print("Jaccard指数为：", Jaccard_index_4)
Dice_index_4 = dice_coefficient(thresh_img4, thresh_seg4)
print("Dice指数为：", Dice_index_4)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
thresh_img4 = cv2.morphologyEx(thresh_img4, cv2.MORPH_OPEN, kernel)
cv2.imshow('thresh_img1', thresh_img4)
cv2.imshow('thresh_seg1', thresh_seg4)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image1")
Jaccard_index_1 = jaccard_index(thresh_img4, thresh_seg4)
print("Jaccard指数为：", Jaccard_index_1)
Dice_index_1 = dice_coefficient(thresh_img4, thresh_seg4)
print("Dice指数为：", Dice_index_1)
