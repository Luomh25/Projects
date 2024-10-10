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

# img1
# 读取图像
img1 = cv2.imread('Image1.png')
seg1 = cv2.imread('Seg1.png')

# 将图像转换为灰度图像
gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray_seg1 = cv2.cvtColor(seg1, cv2.COLOR_BGR2GRAY)

# 应用阈值
ret_img1, thresh_img1 = cv2.threshold(gray_img1, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
ret_seg1, thresh_seg1 = cv2.threshold(gray_seg1, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# 显示结果
cv2.imshow('image1', gray_img1)
cv2.imshow('seg1', gray_seg1)
cv2.imshow('thresh_img1', thresh_img1)
cv2.imshow('thresh_seg1', thresh_seg1)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image1")
Jaccard_index_1 = jaccard_index(thresh_img1, thresh_seg1)
print("Jaccard指数为：", Jaccard_index_1)
Dice_index_1 = dice_coefficient(thresh_img1, thresh_seg1)
print("Dice指数为：", Dice_index_1)
index_1 = (Jaccard_index_1 + Dice_index_1)/2
print("平均分割效果为：", index_1)

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
cv2.imshow('image2', gray_img2)
cv2.imshow('seg2', gray_seg2)
cv2.imshow('thresh_img2', thresh_img2)
cv2.imshow('thresh_seg2', thresh_seg2)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image2")
Jaccard_index_2 = jaccard_index(thresh_img2, thresh_seg2)
print("Jaccard指数为：", Jaccard_index_2)
Dice_index_2 = dice_coefficient(thresh_img2, thresh_seg2)
print("Dice指数为：", Dice_index_2)
index_2 = (Jaccard_index_2 + Dice_index_2)/2
print("平均分割效果为：", index_2)

# img3
# 读取图像
img3 = cv2.imread('Image3.png')
seg3 = cv2.imread('Seg3.png')

# 将图像转换为灰度图像
gray_img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
gray_seg3 = cv2.cvtColor(seg3, cv2.COLOR_BGR2GRAY)

# 应用阈值
ret_img3, thresh_img3 = cv2.threshold(gray_img3, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
ret_seg3, thresh_seg3 = cv2.threshold(gray_seg3, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# 显示结果
cv2.imshow('image3', gray_img3)
cv2.imshow('seg3', gray_seg3)
cv2.imshow('thresh_img3', thresh_img3)
cv2.imshow('thresh_seg3', thresh_seg3)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image3")
Jaccard_index_3 = jaccard_index(thresh_img3, thresh_seg3)
print("Jaccard指数为：", Jaccard_index_3)
Dice_index_3 = dice_coefficient(thresh_img3, thresh_seg3)
print("Dice指数为：", Dice_index_3)
index_3 = (Jaccard_index_3 + Dice_index_3)/2
print("平均分割效果为：", index_3)

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
cv2.imshow('image4', gray_img4)
cv2.imshow('seg4', gray_seg4)
cv2.imshow('thresh_img4', thresh_img4)
cv2.imshow('thresh_seg4', thresh_seg4)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Image4")
Jaccard_index_4 = jaccard_index(thresh_img4, thresh_seg4)
print("Jaccard指数为：", Jaccard_index_4)
Dice_index_4 = dice_coefficient(thresh_img4, thresh_seg4)
print("Dice指数为：", Dice_index_4)
index_4 = (Jaccard_index_4 + Dice_index_4)/2
print("平均分割效果为：", index_4)
