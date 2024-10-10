function images = LoadMNISTImages(filename)
% 读取数据中的图像数据
%   filename为图像数据集名称，images为返回的图像集，
%   为 （28*28）*图像数目 的一个二维矩阵
 
fp = fopen(filename,'rb');% 以二进制方式读取文件
assert(fp~=-1,['Could not open',filename,'']);% 打开文件出错时，fp值为-1
% assert函数，判定是否符合条件，不符合条件，报出错误信息
 
magic = fread(fp,1,'int32',0,'ieee-be');% 从二进制文件中读取数据
% 以int32（32位 整数型）的精度，从fp中读取以无符号字符型一个元素到magic中，
% 待读取字节的排列方式为b,即'ieee-be',即低位字节排放在内存的高地址端，高位字节排放在内存的低地址端
assert(magic==2051,['Bad magic number in',filename,'']);
% 在MNIST图像数据集中，magic值为2051，不为2051的话报错
 
numimages = fread(fp,1,'int32',0,'ieee-be');% 同magic的读取方式，获得图像数目
numrows = fread(fp,1,'int32',0,'ieee-be');% 读取图像的行数
numcols = fread(fp,1,'int32',0,'ieee-be');% 读取图像的列数
 
images = fread(fp,inf,'unsigned char');
% 以"unsigned char"的精度读取剩余的所有像素数据，并存入列向量images中
images = reshape(images,numcols,numrows, numimages);
% 像素值存储时是行优先存储的，而在matlab中，是列优先存储的，故将其重新整合成三维数组时，按照col，row，number的顺序
images = permute(images,[2 1 3]);
% 将之前的三维数组的维度重新整理，得到28*28*图像数目的所有图像数据构成的三维矩阵
 
fclose(fp);% 关闭文件
 
images = reshape(images,size(images,1)*size(images,2),size(images,3));
% 转变成二维向量，每一列代表一个图像，以列优先的方式展开成向量，一个pixel*example数量的矩阵
images = double(images/255);
% convert to double and rescale to [0,1] 归一化
 
end