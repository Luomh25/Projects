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

# 读取图像
print("Image1")
img1 = cv2.imread('Image1.png')
seg1 = cv2.imread('Seg1.png')

# 将图像转换为灰度图像
gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray_seg1 = cv2.cvtColor(seg1, cv2.COLOR_BGR2GRAY)

# 应用Canny边缘检测
edges_img1 = cv2.Canny(gray_img1, 100, 200)
edges_seg1 = cv2.Canny(gray_seg1, 100, 200)

# 显示结果
cv2.imshow('image', img1)
cv2.imshow('seg', seg1)
cv2.imshow('edges_img1', edges_img1)
cv2.imshow('edges_seg1', edges_seg1)
cv2.waitKey(0)
cv2.destroyAllWindows()

Jaccard_index_1 = jaccard_index(edges_img1, edges_seg1)
print("Jaccard指数为：", Jaccard_index_1)
Dice_index_1 = dice_coefficient(edges_img1, edges_seg1)
print("Dice指数为：", Dice_index_1)
index_1 = (Jaccard_index_1 + Dice_index_1)/2
print("平均分割效果为：", index_1)
