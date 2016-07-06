import haitai
import os
import sys
import numpy as np

nan=float('nan')

def subset(th,bk='沪深') :
    if bk == '全部' :
        return th
    if bk =='沪深' :
        return {x for x in th if x[:3]!='002'}
    if bk =='中小' :
        y= {x for x in th if x[:3]=='002'}
        return y

def recent_n_days(n):
    # 得到最近n个交易日日期
    data_dir=haitai.daily_dir
    index300=os.path.join(data_dir,'000001.ss')
    x=list(open(index300))[1:1+n]

    dates=[a.split(',')[0] for a in x]
    return dates

# some math
def mean_with_nan(vecs):
    m=[0 for i in range(len(vecs[0]))]
    nn=[0 for i in range(len(vecs[0]))]

    for vec in vecs:
        for i in range(len(vec)):
            if np.isnan(vec[i]) :
                continue
            nn[i]+=1
            m[i]+=vec[i]
    m=[a/b if b>0 else np.nan for a,b in zip(m,nn)]
    return np.array(m)

def mean_and_var_with_nan(vecs):
    # 求均值方差
    m=[0 for i in range(len(vecs[0]))] # mean 
    m2=[0 for i in range(len(vecs[0]))] # 方差
    nn=[0 for i in range(len(vecs[0]))] # number of non-non elements

    for vec in vecs:
        for i in range(len(vec)):
            if np.isnan(vec[i]) :
                continue
            nn[i]+=1
            m[i]+=vec[i]
    m=[a/b if b>0 else np.nan for a,b in zip(m,nn)]

    for vec in vecs:
        for i in range(len(vec)):
            if np.isnan(vec[i]) :
                continue
            m2[i]+=(vec[i]-m[i])**2
    m2=[a/b if b>0 else np.nan for a,b in zip(m2,nn)]
    m2=np.array(m2)
    return np.array(m),m2



def gen_vec(lines,n,ind=3):
    i=n
    
    for i in range(n,len(lines)):
        t=lines[i].split(',')[ind]
        if not t : break
        if float(t)!=0 : break
    x=lines[:i+1]
    days=[a.split(',') for a in x]
    kv=[[x[0],float(x[ind])] for x in days]
    for i in range(len(kv)-1):
        pass
        if kv[-1-i-1][1]==0 : kv[-1-i-1][1]=float('nan')
    kv=kv[:n]
    return kv



def gen_price(lines,n,vind=11,use_nan=True,nov=False):
    # 得到163daily文件中的价格一列
    # lines : raw data except the first line
    # vind  : ind of the column
    # n     : recent n days 
    ind=3
    i=n
    
    x=lines[:n]
    days=[a.split(',') for a in x]

    if nov==False :
        days=[[x[0],x[3],float(x[7]),float(x[vind])] for x in days]
    else :
        days=[[x[0],x[3],float(x[7]),1] for x in days]

    k=1
    last=None
    for i,day in enumerate(days) :
        flag=False
        if day[1]=='' or day[1]=='0.0': 
            flag=True

            day[1]=day[2]
        else : 
            day[1]=float(day[1])
        if last==None :
            last=day[2]
        else :
            if last!=day[1] :
                k=k*day[1]/last
                pass
            last=day[2]
        day[1]/=k
        if flag  and use_nan : day[1]=nan
        if day[3]==0 : day[3]=nan

    return [[x[0],x[1],x[3]] for x in days]


def load_stock_set(stock_set,ndays,dates,vol_ind=10):
    """
    vol_ind=10 # 换手率
    vol_ind=11 # 成交量
    """
    files=os.listdir(haitai.daily_dir)
    files=[[file,os.path.join(haitai.daily_dir,file)] for file in files]
    files=sorted(files)

    pss=[]
    vols=[]
    for f,v in files:
        k,tp=f.split('.')
        if f not in stock_set : continue
        
        raw=list(open(v))[1:]
        vec=gen_price(raw,ndays,use_nan=False)
        if vec[-1][0]!=dates[-1] : 
            print('dates not matched',k)
            continue

        ps=np.array([p for d,p,*_ in vec])
        ps=ps/ps[0]

        if any(np.isnan(x) for x in ps) : 
            print('nan',k)
            continue

        pss.append(ps)
        print(k,end='\r')

        vol=gen_vec(raw,ndays,ind=vol_ind)
        vol=np.array([p for d,p in vol])
        vols.append(vol)
    return pss,vols


def moving_average(price,n=2):
    p2=np.array(price.tolist()[1:]+[price[-1]])
    p3=np.array(price.tolist()[2:]+[price[-1]]*2)
    return (price+p2+p3)/2
