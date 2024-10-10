import cv2
import numpy as np

def gaussian_filter(img, ksize=3, sigma=1.5):
    return cv2.GaussianBlur(img, (ksize, ksize), sigma)

def median_filter(img, ksize=3):
    return cv2.medianBlur(img, ksize)

def region_growing(img, seed):
    threshold = 66
    seed_value = img[seed[0], seed[1]]
    rows, cols = img.shape[:2]
    segmented = np.zeros_like(img)
    segmented[seed[0], seed[1]] = 255
    queue = []
    queue.append(seed)
    while queue:
        current_point = queue.pop(0)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if current_point[0] + i < 0 or current_point[0] + i >= rows or current_point[1] + j < 0 or \
                        current_point[1] + j >= cols:
                    continue
                diff = abs(int(img[current_point[0] + i, current_point[1] + j]) - int(seed_value))
                if diff < threshold and segmented[current_point[0] + i, current_point[1] + j] == 0:
                    segmented[current_point[0] + i, current_point[1] + j] = 255
                    queue.append((current_point[0] + i, current_point[1] + j))
    return segmented

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
print("Image2")
img2 = cv2.imread('Image2.png')
seg2 = cv2.imread('Seg2.png')
height2, width2, channels2 = img2.shape
print('Image size: {} x {} pixels'.format(width2, height2))

# 将图像转换为灰度图像
gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
gray_seg2 = cv2.cvtColor(seg2, cv2.COLOR_BGR2GRAY)

gray_img2 = gaussian_filter(gray_img2, ksize=3, sigma=1.5)
gray_seg2 = gaussian_filter(gray_seg2, ksize=3, sigma=1.5)
#gray_img2 = median_filter(gray_img2, ksize=3)
#gray_seg2 = median_filter(gray_seg2, ksize=3)

# 选取种子点
x2, y2 = 150, 145
pixel_value = img2[y2, x2]
print('Pixel value at ({}, {}): {}'.format(x2, y2, pixel_value))
seed2 = (x2, y2)

# 进行区域增长
sgtd_img2 = region_growing(gray_img2, seed2)
sgtd_seg2 = region_growing(gray_seg2, seed2)

#sgtd_img2 = gaussian_filter(sgtd_img2, ksize=3, sigma=1.5)
#sgtd_seg2 = gaussian_filter(sgtd_seg2, ksize=3, sigma=1.5)
sgtd_img2 = median_filter(sgtd_img2, ksize=3)
sgtd_seg2 = median_filter(sgtd_seg2, ksize=3)

# 显示分割结果
cv2.imshow('image2', gray_img2)
cv2.imshow('seg2', gray_seg2)
cv2.imshow('sgtd_img2', sgtd_img2)
cv2.imshow('sgtd_seg2', sgtd_seg2)
cv2.waitKey(0)
cv2.destroyAllWindows()

Jaccard_index_2 = jaccard_index(sgtd_img2, sgtd_seg2)
print("Jaccard指数为：", Jaccard_index_2)
Dice_index_2 = dice_coefficient(sgtd_img2, sgtd_seg2)
print("Dice指数为：", Dice_index_2)
index_2 = (Jaccard_index_2 + Dice_index_2)/2
print("平均分割效果为：", index_2)
