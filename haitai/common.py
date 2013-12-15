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
    data_dir='data/163_daily'
    index300=os.path.join(data_dir,'000001.ss')
    x=list(open(index300))[1:1+n]

    dates=[a.split(',')[0] for a in x]
    return dates

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



def gen_price(lines,n,vind=11,use_nan=True):
    ind=3
    i=n
    
    x=lines[:n]
    days=[a.split(',') for a in x]
    days=[[x[0],x[3],float(x[7]),float(x[vind])] for x in days]

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
    


