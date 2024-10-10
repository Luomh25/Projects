import cv2
import numpy as np

# 定义 Jaccard 系数计算函数
def jaccard_index(img1, img2):
    intersection = np.logical_and(img1, img2)
    union = np.logical_or(img1, img2)
    jaccard_index = np.sum(intersection) / np.sum(union)
    return jaccard_index

# 读取图像
image = cv2.imread("Image1.png")

# 将图像转换为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用 Canny 边缘检测器检测边缘
edges = cv2.Canny(gray, 100, 200)

# 对边缘进行膨胀操作
kernel = np.ones((5, 5), np.uint8)
dilated_edges = cv2.dilate(edges, kernel, iterations=1)

# 使用连续组件分析将图像分割成不同的区域
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilated_edges)

# 定义真实标签图像
label = cv2.imread("Seg1.png", cv2.IMREAD_GRAYSCALE)

# 将分割结果转换为二值图像并计算 Jaccard 系数
jaccard_scores = []
for i in range(1, num_labels):
    mask = np.zeros_like(gray, dtype=np.uint8)
    mask[labels == i] = 255
    seg_binary = np.zeros_like(mask)
    seg_binary[mask > 0] = 1
    label_binary = np.zeros_like(label)
    label_binary[label > 0] = 1
    jaccard_score = jaccard_index(seg_binary, label_binary)
    jaccard_scores.append(jaccard_score)
    result = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow(f"Segment {i}", result)

# 输出平均 Jaccard 系数
mean_jaccard_score = np.mean(jaccard_scores)
print(f"Mean Jaccard score: {mean_jaccard_score}")

cv2.waitKey(0)
cv2.destroyAllWindows()