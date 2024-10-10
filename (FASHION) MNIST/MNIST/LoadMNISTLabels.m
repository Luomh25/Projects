function labels = LoadMNISTLabels(filename)
% 读取数据中的标记数据
%   filename为标记label数据集名称，labels为返回的图像的标记值
%   为 图像数目*1 的一个矩阵
 
fp = fopen(filename,'rb');% 以二进制方式读取文件
assert(fp~=-1,['Could not open',filename,'']);% 打开文件出错时，fp值为-1
% assert函数，判定是否符合条件，不符合条件，报出错误信息
 
magic = fread(fp,1,'int32',0,'ieee-be');% 从二进制文件中读取数据
% 以int32（32位 整数型）的精度，从fp中读取一个元素到magic中，
% 待读取字节的排列方式为b,即'ieee-be',即低位字节排放在内存的高地址端，高位字节排放在内存的低地址端
assert(magic==2049,['Bad magic number in',filename,'']);
% 在MNIST标签数据集中，magic值为2049，不为2049的话报错
 
numlabels = fread(fp,1,'int32',0,'ieee-be');% 同magic的读取方式，获得标签数目
 
labels = fread(fp,inf,'unsigned char');
% 以"unsigned char"的精度读取剩余的所有标签数据，并存入列向量labels中
 
assert(size(labels,1)==numlabels,'Mismatch in label count');
% 判断读取出的标签个数是否与文件中保存的标签数目相同，不同则报错
 
fclose(fp);% 关闭文件
 
end
 