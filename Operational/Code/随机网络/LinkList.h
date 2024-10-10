//LinkList.h  声明类LinkList
#ifndef LinkList_H
#define LinkList_H
#include <deque>
#include <cassert>
#include <vector>
#include <cstring>
#include <array>
#include <algorithm>
#include <random>
#include <cmath>
#include <numeric>
#include <fstream>

struct Friend
{
  int name;
  unsigned char decision;
  Friend *next=NULL;
};

struct Node
{
  //int name;//用序号表示名字
  double Value[4];//用于存储stratsW、stratsa、stratsV、stratsb四个数据
  int Friendnum=0;
  double fenshu=0;
  double E_fenshu=0;
  unsigned char decision;
  Friend *first=NULL;
};


class LinkList
{
  public:
    LinkList( );  //建立只有头结点的空链表
    ~LinkList();             //析构函数
    int E_pay(double per, double nei, double W, double V);//计算per的期望决策
    void pengyou(int i,int j);//输入i、j两个人，两个人的朋友矩阵各自加1个结点
    void fuzhi(int i,double b[4]);//给第i个人赋予4种感情
    double getW(int i);//提取第i个人的感情特征这一数据
    double geta(int i);//提取第i个人的感情特征这一数据
    double getV(int i);//提取第i个人的感情特征这一数据
    double getb(int i);//提取第i个人的感情特征这一数据
    void xiugai(int i,int m,double b);//修改第i个人的第m种情感
    void defen(int i);//当抽到第i个人时，计算抽取第i个人的得分
    void E_defen(int i);//当抽到第i个人时，计算抽取第i个人的期望得分
    void qinggan(int i);//第i个人步骤结束时，对其进行情感更新。
    double getfenshu(int i);//取出第i个人的分数
    double getE_fenshu(int i);//取出第i个人的期望分数
    double getFriendnum(int i);//取出第i个人的分数
    void xiugaifenshu(int i,double j);//修改第i个人的得分为j；
    void xiugaiE_fenshu(int i,double j);//修改第i个人的期望得分为j；
    unsigned char strategy(double per, double nei, double W, double V, double a, double b, double p1, double p2);//计算玩家决策
    double payoff(unsigned char a, unsigned char b);//计算i的收益情况
    void qinggan_cnt();//在蒙特卡洛步之后统计各个情感的人数
    int qinggan_change();//计算一个蒙特卡洛步后，各种情感的人数变化之和
    int * getValueshuliang();//返回Valueshuliang的值

    void MonteCarlo();//开始一个蒙特卡洛步，这是一个打包操作的函数


 private:
   Node a[2500];//node链表
   int pastValueshuliang[5][4];//用于记录上五个蒙特卡洛步各种类型的人的数量
   int Valueshuliang[4];//用于统计各种类型的人的数量
};

#endif






/*


template <class T>
class LinkList
{
  public:
    LinkList( );  //建立只有头结点的空链表
    LinkList(T a[ ], int n);  //建立有n个元素的单链表
    ~LinkList();             //析构函数
    int Length();          //求单链表的长度
    T Get(int i);           //取单链表中第i个结点的元素值
    int Locate(T x);       //求单链表中值为x的元素序号
    void Insert(int i, T x);   //在单链表中第i个位置插入元素值为x的结点
    void Insert2(T x);   //在单链表中第i个位置插入元素值为x的结点
    T Delete(int i);        //在单链表中删除第i个结点
    void PrintList( );           //遍历单链表，按序号依次输出各元素
 private:
   Node<T> *first;  //单链表的头指针
};

#endif
*/