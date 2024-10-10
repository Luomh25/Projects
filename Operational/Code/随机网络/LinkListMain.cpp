//LinkListMain.cpp
#include <iostream>  //引用输入输出流库函数的头文件
#include "LinkList.cpp"  //引用单链表的类
using namespace std;

int a[2500][2500];
int main( )
{
  random_device rd; // 生成随机数种子
  mt19937 g(rd()); // 生成随机数生成器
  uniform_int_distribution <> dir(0, 1); // 生成均匀分布的实数随机数，范围为 [0, 1]
  uniform_real_distribution <double> q1(0.0, 1.0); // 生成均匀分布的实数随机数，范围为 [0, 1]
  uniform_real_distribution <double> q2(0.0, 1.0); // 生成均匀分布的实数随机数，范围为 [0, 1]

  LinkList test;

  //先对每个人的情感赋值
  for(int ii=0;ii<2500;ii++)
  {

    int x1=dir(g);
    int x2=dir(g);
    double y1=q1(g);
    double y2=q2(g);
    double c[4];
    c[0]=x1;
    c[1]=y1;
    c[2]=x2;
    c[3]=y2;
    test.fuzhi(ii,c);
  }
  
  //再确定朋友关系！！！！！！
  //生成随机朋友矩阵
  double p=0.0016;//随机网络生成朋友的概率  //由网络度数产生
  for (int i=0;i<2500;i++)
  {
    for(int j=i+1;j<2500;j++)
    {
      double p1=q1(g);
      if(p1<p)
      {
        a[i][j]=1;
      }
      else
      {
        a[i][j]=0;
      }
    }
  }

//将随机朋友矩阵转化为朋友链表
  for (int i=0;i<2500;i++)
  {
    for(int j=i+1;j<2500;j++)
    {
      if(a[i][j]==1)
      {
        test.pengyou(i,j);
      }
    }
  }

  cout<<"朋友关系建立完毕1111111"<<endl;
  
  test.MonteCarlo();
}