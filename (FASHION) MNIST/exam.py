# coding utf-8
from sklearn.ensemble import \
    RandomForestClassifier  # 随机森林分类器
from sklearn.datasets import \
    load_digits  # 数据集
from sklearn.model_selection import \
    train_test_split  # 数据分割模块
from sklearn.metrics import \
    classification_report  # 生产报告
from sklearn.metrics import confusion_matrix
import numpy as np
import struct
import matplotlib.pyplot as plt
import pandas as pd

# 1.加载数据
# 训练集文件
train_images_idx3_ubyte_file = 'E:/2023/数图/hw/MNIST/train-images.idx3-ubyte'
# 训练集标签文件
train_labels_idx1_ubyte_file = 'E:/2023/数图/hw/MNIST/train-labels.idx1-ubyte'
# 测试集文件
test_images_idx3_ubyte_file = 'E:/2023/数图/hw/MNIST/t10k-images.idx3-ubyte'
# 测试集标签文件
test_labels_idx1_ubyte_file = 'E:/2023/数图/hw/MNIST/t10k-labels.idx1-ubyte'

def decode_idx3_ubyte(idx3_ubyte_file):
    # 读取二进制数据
    bin_data = open(idx3_ubyte_file, 'rb').read()
    # 解析文件头信息，依次为魔数、图片数量、每张图片高、每张图片宽
    offset = 0
    fmt_header = '>iiii'   #'>IIII'是说使用大端法读取4个unsinged int32
    magic_number, num_images, num_rows, num_cols = struct.unpack_from(fmt_header, bin_data, offset)
    print('魔数:%d, 图片数量: %d张, 图片大小: %d*%d' % (magic_number, num_images, num_rows, num_cols))

    # 解析数据集
    image_size = num_rows * num_cols
    offset += struct.calcsize(fmt_header)
    print("offset: ",offset)
    fmt_image = '>' + str(image_size) + 'B'   # '>784B'的意思就是用大端法读取784个unsigned byte
    images = np.empty((num_images, num_rows*num_cols))
    for i in range(num_images):
        if (i + 1) % 10000 == 0:
            print('已解析 %d' % (i + 1) + '张')
        images[i] = np.array(struct.unpack_from(fmt_image, bin_data, offset)).reshape((num_rows*num_cols))
        offset += struct.calcsize(fmt_image)
    return images.T


def decode_idx1_ubyte(idx1_ubyte_file):
    # 读取二进制数据
    bin_data = open(idx1_ubyte_file, 'rb').read()
    # 解析文件头信息，依次为魔数和标签数
    offset = 0
    fmt_header = '>ii'
    magic_number, num_images = struct.unpack_from(fmt_header, bin_data, offset)
    print('魔数:%d, 图片数量: %d张' % (magic_number, num_images))

    # 解析数据集
    offset += struct.calcsize(fmt_header)
    fmt_image = '>B'
    labels = np.empty(num_images)
    for i in range(num_images):
        if (i + 1) % 10000 == 0:
            print('已解析 %d' % (i + 1) + '张')
        labels[i] = struct.unpack_from(fmt_image, bin_data, offset)[0]
        offset += struct.calcsize(fmt_image)
    return labels


def load_train_images(idx_ubyte_file=train_images_idx3_ubyte_file):
    return decode_idx3_ubyte(idx_ubyte_file)


def load_train_labels(idx_ubyte_file=train_labels_idx1_ubyte_file):
    return decode_idx1_ubyte(idx_ubyte_file)


def load_test_images(idx_ubyte_file=test_images_idx3_ubyte_file):
    return decode_idx3_ubyte(idx_ubyte_file)


def load_test_labels(idx_ubyte_file=test_labels_idx1_ubyte_file):
    return decode_idx1_ubyte(idx_ubyte_file)

x_train = load_train_images()
#(num_rows*num_cols,num_images)
y_train = load_train_labels()
x_test = load_test_images()
y_test = load_test_labels()

# 查看前十个数据及其标签以读取是否正确
for i in range(10):
    print(y_train[i])
    #plt.imshow(y_train[i], cmap='gray')
    #plt.show()
print('done')

for i in range(10):
    print(x_train[i])
    #plt.imshow(y_train[i], cmap='gray')
    #plt.show()
print('done')