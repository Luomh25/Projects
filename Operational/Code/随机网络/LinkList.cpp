//LinkList.cpp
#include "LinkList.h"
#include "Math.h"
#include <iostream>  //引用输入输出流库函数的头文件
using namespace std;


const unsigned char D = 0; //背叛
const unsigned char C = 1; //合作
const unsigned char B = -1; //漠然
const double threshold = 5;

//const double WMIN = 0.1;
//const double WMAX = 1.0;

const double K = 0.1;
//double M = 5;

double R = 1;
double S = 0;
double T = 1.5;
double P = 0;
double sig = 0.3;


LinkList:: LinkList()
{
//  Node a[2500];  //2500个人
//  first=a;
for(int i=0;i<4;i++)
{
  Valueshuliang[i]=0;
}
for(int i=0;i<5;i++)
{
  for(int j=0;j<4;j++)
  {
    pastValueshuliang[i][j]=0;
  }
}
for(int i=0;i<2500;i++)
{
  this->a[i].fenshu=0;
  this->a[i].E_fenshu=0;
  this->a[i].first=NULL;
  this->a[i].Friendnum=0;
}
}

LinkList:: ~LinkList()
{
  
}

int LinkList::E_pay(double per, double nei, double W, double V)
{
    if (per >= nei)
    {
        if (W == 0)
            return 10;
        else
            return 11;
    }
    else
    {
        if (V == 0)
            return 0;
        else
            return 1;
    }
}



// 根据收益率和邻居的收益率，以及策略参数，返回当前玩家的策略
unsigned char LinkList::strategy(double per, double nei, double W, double V, double a, double b, double p1, double p2)
{
    if (per >= nei){
        if (W == 0){
            if (p1 <= a) return C; //合作
            else return B; //漠然
        }
        else{
            if (p1 <= a) return D; //背叛
            else return B; //漠然
        }
    }
    else {
        if (V == 0){
            if (p2 <= b) return C; //合作
            else return B; //漠然
        }
        else{
            if (p2 <= b) return D; //背叛
            else return B; //漠然
        }
    }
}

// 根据两个玩家的策略，返回它们的收益
double LinkList::payoff(unsigned char a, unsigned char b)
{
    if (a == D && b == D) 
        return P;
    if (a == D && b == C) 
        return T;
    if (a == C && b == D) 
        return S;
    if (a == C && b == C)
        return R;
    if (a == B || b == B)
        return sig;
    return 0;
}







void LinkList::fuzhi(int i,double b[4])
{
  for(int j=0;j<=3;j=j+1)
  this->a[i].Value[j]=b[j];
}

void LinkList::pengyou(int i,int j)
{
  Friend *p=new Friend;Friend *q=new Friend;
  p->name=j;q->name=i;
  // p->next=NULL;q->next=NULL;  
  p->next=this->a[i].first;
  q->next=this->a[j].first;
  this->a[i].first=p;
  this->a[j].first=q;
  this->a[i].Friendnum++;
  this->a[j].Friendnum++;
}


double LinkList::getW(int i)//提取每个人的感情特征这一数据
{
  double b;
  b=this->a[i].Value[0];
  return b;
}
double LinkList::getV(int i)
{
  double b;
  b=this->a[i].Value[2];
  return b;
}
double LinkList::geta(int i)
{
  double b;
  b=this->a[i].Value[1];
  return b;
}
double LinkList::getb(int i)
{
  double b;
  b=this->a[i].Value[3];
  return b;
}

double LinkList::getfenshu(int i)
{
  double b;
  b=this->a[i].fenshu;
  return b;
}

double LinkList::getE_fenshu(int i)
{
  double b;
  b=this->a[i].E_fenshu;
  return b;
}

double LinkList::getFriendnum(int i)
{
  double b;
  b=this->a[i].Friendnum;
  return b;
}

void LinkList::xiugai(int i,int m,double b)
{
  this->a[i].Value[m]=b;
}

void LinkList::xiugaifenshu(int i,double j)
{
  this->a[i].fenshu=j; 
}

void LinkList::xiugaiE_fenshu(int i,double j)
{
  this->a[i].E_fenshu=j; 
}


void LinkList::defen(int i)//当抽到第i个人时，计算抽取第i个人的得分
{
  //用循环，找到i的每一个朋友j，用j得到其情感类型，计算i的得分情况，
  //一路加下来后，将总分记在i的fenshu中。
  //
  random_device rd; // 生成随机数种子
  mt19937 g(rd()); // 生成随机数生成器
  uniform_real_distribution <double> P1(0.0, 1.0); // 生成均匀分布的实数随机数，范围为 [0, 1]
  uniform_real_distribution <double> P2(0.0, 1.0); // 生成均匀分布的实数随机数，范围为 [0, 1]
  Node q1=this->a[i];
  Friend * p=q1.first;
  double pay=0;
  while(p!=NULL)
  {
    int j=p->name;
    Node q2=this->a[j];
    unsigned char ans1=strategy(q1.fenshu,q2.fenshu,getW(i),getV(i),geta(i),getb(i),P1(g),P2(g));
    unsigned char ans2=strategy(q2.fenshu,q1.fenshu,getW(j),getV(j),geta(j),getb(j),P1(g),P2(g));
    p->decision = ans1;
    Friend *t=q2.first;
    while(t->name!=i)
    {
      t=t->next;
    }
    t->decision = ans2;
    pay=pay+payoff(ans1,ans2);
    p=p->next;
  }
  if (q1.Friendnum != 0)
  {
    pay=pay/q1.Friendnum;
    xiugaifenshu(i,pay);
  }
  else
  {
    xiugaifenshu(i,0);
  }
}

void LinkList::E_defen(int i)//当抽到第i个人时，计算抽取第i个人的期望得分
{
  Node q1=this->a[i];
  
  Friend * p=q1.first;
  double pay_last_i=getfenshu(i);
  double Epay=0;
  while(p!=NULL)
  {
    int j=p->name;
    Node q2=this->a[j];
    double pay_last_j=getfenshu(j);

    int tem = E_pay(pay_last_i,pay_last_j,getW(i), getV(j)); 
                if (tem == 10){
                    if (getV(j) == 0){
                        double p_R = geta(i) * getb(j);
                        Epay += R * p_R + sig *(1-p_R);
                    }
                    else{
                        double p_S = geta(i) * getb(j);
                        Epay += S * p_S + sig *(1-p_S);
                    }
                }
                if (tem == 11){
                    if (getV(j) == 0){
                        double p_T = geta(i) * getb(j);
                        Epay += T * p_T + sig *(1-p_T);
                    }
                    else{
                        double p_P = geta(i) * getb(j);
                        Epay += P * p_P + sig *(1-p_P);
                    }
                }
                if (tem == 0){
                    if (getW(j) == 0){
                        double p_R = getb(i) * geta(j);
                        Epay += R * p_R + sig *(1-p_R);
                    }
                    else{
                        double p_S = getb(i) * geta(j);
                        Epay += S * p_S + sig *(1-p_S);
                    }
                }
                if (tem == 1){
                    if (getW(j) == 0){
                        double p_T = geta(i) * getb(j);
                        Epay += T * p_T + sig *(1-p_T);
                    }
                    else{
                        double p_P = geta(i) * getb(j);
                        Epay += P * p_P + sig *(1-p_P);
                    }
                }
    p=p->next;
  }
  if(q1.Friendnum!=0)
  {
    Epay=Epay/q1.Friendnum;
    xiugaiE_fenshu(i,Epay);
  }
  else
  {
    xiugaiE_fenshu(i,0);
  }
}



void LinkList::qinggan(int i)
{
  
  random_device rd; // 生成随机数种子
  mt19937 g(rd()); // 生成随机数生成器
  uniform_real_distribution <> dir(0, 1); // 生成均匀分布的实数随机数，范围为 [0, 1]
  uniform_real_distribution <double> r1(0.0, 1.0); // 生成均匀分布的实数随机数，范围为 [0, 1]
  uniform_real_distribution <double> r2(0.0, 1.0); // 生成均匀分布的实数随机数，范围为 [0, 1]
  int fn=getFriendnum(i);
  double dd= dir(g)*fn;
  int d=floor(dd);//去尾，得到学习的朋友的排位，从0开始，到fn-1结束，共fn个朋友
  if(dd==fn)d=fn-1;

  Friend * p=this->a[i].first;
  if(d!=0)
  {
    for(int j=1;j<=d;j++)
    {
      p=p->next;
    }
  }
  int s=0;
  if(p==NULL) return;
  else s=p->name;//g是第i个人的第d个朋友，即要学习的朋友

  double wx = 1;
  //double Dp = getfenshu(i)-getfenshu(s);
  double Dp = getE_fenshu(i)-getE_fenshu(s);
  double q = wx / (1.0 + exp(Dp / K));
  double r_1 = r1(g);
  double r_2 = r2(g);
  if (r_1 <= q && r_2 > q)
  {
    xiugai(i,0,getW(s));
    xiugai(i,1,geta(s));
  } 
  else if (r_1 > q && r_2 <= q)
  {
    xiugai(i,2,getV(s));
    xiugai(i,3,getb(s));
  } 
  else if (r_1 <= q && r_2 <= q)
  {
    xiugai(i,0,getW(s));
    xiugai(i,1,geta(s));
    xiugai(i,2,getV(s));
    xiugai(i,3,getb(s));
  } 
}


void LinkList::qinggan_cnt()
{
  for(int i=0;i<4;i++)
  {
    for(int j=0;j<4;j++)
    {
      pastValueshuliang[i][j]=pastValueshuliang[i+1][j];
    }
  }
  for(int i=0;i<4;i++)
  {
    pastValueshuliang[4][i]=0;
    Valueshuliang[i]=0;
  }
  for(int i=0;i<2500;i++)
  {
    if (getW(i) == 1 && getV(i) == 1) ++Valueshuliang[0];
    if (getW(i) == 0 && getV(i) == 1) ++Valueshuliang[1];
    if (getW(i) == 1 && getV(i) == 0) ++Valueshuliang[2];
    if (getW(i) == 0 && getV(i) == 0) ++Valueshuliang[3];
  }
  for(int i=0;i<4;i++)
  {
    pastValueshuliang[4][i]=Valueshuliang[i];
  }
}

int LinkList::qinggan_change()
{
  int b=0;
  for(int i=0;i<4;i++)
  {
    for(int j=0;j<4;j++)
    b=b+abs(pastValueshuliang[i][j]-pastValueshuliang[i+1][j]);
  }
  return b;
}

int * LinkList::getValueshuliang()//返回Valueshuliang的值
{
  int *b;
  b=new int[4];
  for(int i=0;i<4;i++)
  {
    b[i]=this->Valueshuliang[i];
  }
  return b;
}






void LinkList::MonteCarlo()
{
  /*for(int yest=0;yest<2500;yest++)
      {
        cout<<getfenshu(yest)<<endl;
      }*/
  ofstream outfile("output_E3.txt");
  if (!outfile.is_open())
  {
      cout<< "无法打开文件output_E.txt" << endl;
      return;
  }
  outfile << "步数\tP1\tP2\tP3\tP4\t合作\t背叛\t孤独\t平均收益\t平均期望收益\t更新人数"<< endl;


  int count=0;
  random_device rd; // 生成随机数种子
  mt19937 g(rd()); // 生成随机数生成器
  uniform_int_distribution <> dir(0, 2499); // 生成均匀分布的整数随机数，范围为 [0, 2499]
  while(true)
  {
    int change=0;
    count++;
    for (int _iter = 0; _iter < 2500; _iter++)
    {
      int m=dir(g);//对第i个人做蒙特卡洛步
      defen(m);
      
      E_defen(m);
      qinggan(m);
    }
    qinggan_cnt();

    for(int jj=0;jj<4;jj++)
    {
      change+=abs(pastValueshuliang[4][jj]-pastValueshuliang[3][jj]);
    }


    if(count%10==0)
    {
      // 计算情感类型分布
      int *bbbb;
      bbbb=getValueshuliang();
            // 计算策略类型和平均收益
            double avg_pay = 0;
            double avg_E_pay = 0;
            int co = 0;
            int de = 0;
            int lo = 0;
            for (int i = 0; i < 2500; i ++)
            {
              avg_pay += getfenshu(i);
              avg_E_pay += getE_fenshu(i);
              Friend * p=this->a[i].first;
              while(p!=NULL)
              {
                if(p->decision==C)co++;
                if(p->decision==D)de++;
                if(p->decision==B)lo++;
                p=p->next;
              }
            }
            int lonely=0;
            for(int i=0;i<2500;i++)
            {
              if(this->a[i].Friendnum==0)lonely++;
            }
            int ppnum=2500-lonely;
            avg_pay = avg_pay/ppnum;
            avg_E_pay = avg_E_pay/ppnum;
            // 写入数据
            outfile << count << '\t' << bbbb[0] << '\t' << bbbb[1] << '\t' << bbbb[2] << '\t' << bbbb[3] << '\t' << co << '\t' << de << '\t' << lo <<  '\t' << avg_pay <<  '\t' << avg_E_pay << '\t' << change << endl;
    }
  



    if(qinggan_change()<2)
    {
      cout<<"模型收敛"<<'\n';

      cout << "第" << count << "个蒙特卡洛步" << endl;
      int *b;
      b=getValueshuliang();
      cout << b[0] << " " << b[1] << " " << b[2] << " " << b[3] << endl;


      // 计算情感类型分布
      int *bbbb;
      bbbb=getValueshuliang();
            // 计算策略类型和平均收益
            double avg_pay = 0;
            double avg_E_pay = 0;
            int co = 0;
            int de = 0;
            int lo = 0;
            for (int i = 0; i < 2500; i ++)
            {
              avg_pay += getfenshu(i);
              avg_E_pay += getE_fenshu(i);
              Friend * p=this->a[i].first;
              while(p!=NULL)
              {
                if(p->decision==C)co++;
                if(p->decision==D)de++;
                if(p->decision==B)lo++;
                p=p->next;
              }
            }
            int lonely=0;
            for(int i=0;i<2500;i++)
            {
              if(this->a[i].Friendnum==0)lonely++;
            }
            int ppnum=2500-lonely;
            avg_pay = avg_pay/ppnum;
            avg_E_pay = avg_E_pay/ppnum;
            // 写入数据
            outfile << count << '\t' << bbbb[0] << '\t' << bbbb[1] << '\t' << bbbb[2] << '\t' << bbbb[3] << '\t' << co << '\t' << de << '\t' << lo <<  '\t' << avg_pay <<  '\t' << avg_E_pay << '\t' << change << endl;


      
      
      break;
    }
    else if(count>10000)
    {
      cout<<"模型未收敛"<<'\n';
      break;
    }

    cout << "第" << count << "个蒙特卡洛步" << endl;
    int *b;
    b=getValueshuliang();
    cout << b[0] << " " << b[1] << " " << b[2] << " " << b[3] << endl;
  }
}