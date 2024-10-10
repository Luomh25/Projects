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
print("Image3")
img3 = cv2.imread('Image3.png')
seg3 = cv2.imread('Seg3.png')

# 将图像转换为灰度图像
gray_img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
gray_seg3 = cv2.cvtColor(seg3, cv2.COLOR_BGR2GRAY)

# 计算高斯滤波
blur_img3 = cv2.GaussianBlur(gray_img3, (3, 3), 0)
blur_seg3 = cv2.GaussianBlur(gray_seg3, (3, 3), 0)

# 计算图像灰度直方图
hist = cv2.calcHist([blur_seg3], [0], None, [256], [0, 256])

# 寻找最优阈值
total_pixels = blur_seg3.shape[0] * blur_seg3.shape[1]
sum_pix = 0
max_var = 0
best_thresh = 0
for i in range(256):
    sum_pix += i * hist[i]
    w0 = np.sum(hist[:i+1]) / total_pixels
    w1 = 1 - w0
    if w0 == 0 or w1 == 0:
        continue
    mean0 = sum_pix / (w0 * total_pixels)
    mean1 = (np.sum(hist[i+1:] * np.arange(i+1, 256)) / (w1 * total_pixels))
    var = w0 * w1 * (mean0 - mean1) ** 2
    if var > max_var:
        max_var = var
        best_thresh = i

# 应用Canny边缘检测
print(best_thresh)
edges_img3 = cv2.Canny(blur_img3, best_thresh * 0.7, best_thresh * 0.9)
edges_seg3 = cv2.Canny(blur_seg3, best_thresh * 0.7, best_thresh * 0.9)

# 显示结果
cv2.imshow('Image3', gray_img3)
cv2.imshow('Seg3', gray_seg3)
cv2.imshow('edges_img3', edges_img3)
cv2.imshow('edges_seg3', edges_seg3)
cv2.waitKey(0)
cv2.destroyAllWindows()

Jaccard_index_3 = jaccard_index(edges_img3, edges_seg3)
print("Jaccard指数为：", Jaccard_index_3)
Dice_index_3 = dice_coefficient(edges_img3, edges_seg3)
print("Dice指数为：", Dice_index_3)
index_3 = (Jaccard_index_3 + Dice_index_3)/2
print("平均分割效果为：", index_3)
