#!/usr/bin/python3
import os
import sys
import numpy
import math
import random

import haitai
from haitai.common import *

import pylab
import numpy as np

from haitai.graph import *


def plot(data,r_std,vol,vol_std,both_ticks=None):
    xs=list(range(0,-len(data),-1))
    ax=pylab.subplot(2,1,1)
    draw_lines(ax,[[data,'k'],[r_std,'b']],log=True)
    draw_lines(ax,[[data,'k-'],[data,'b,'],],log=True)
    draw_grid(ax,both_ticks)


    ax=pylab.subplot(2,1,2)
    draw_lines(ax,[[vol],[vol_std]])
    draw_grid(ax,both_ticks)



def subset(th,bk='沪深') :
    if bk == '全部' :
        return th
    if bk =='沪深' :
        return {x for x in th if x[:3]!='002'}
    if bk =='中小' :
        y= {x for x in th if x[:3]=='002'}
        return y

def mean_with_nan(vecs):
    m=[0 for i in range(len(vecs[0]))]
    m2=[0 for i in range(len(vecs[0]))]
    nn=[0 for i in range(len(vecs[0]))]

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
    #m2=np.sqrt(m2)
    return np.array(m),m2


if __name__ == '__main__':

    ndays=500
    bk='全部'
    bk='中小'
    bk='沪深'

    pylab.figure(figsize=(12,6))
    dates=recent_n_days(ndays)

    both_ticks=gen_ticks(dates)

    th=set()
    for line in list(open(haitai.stock_ids)): ## first three is not 
        line=line.strip()
        th.add(line)
    th=subset(th,bk)
    
    files=os.listdir(haitai.daily_dir)
    files=[[file,os.path.join(haitai.daily_dir,file)] for file in files]
    files=sorted(files)


    pss=[]
    vols=[]
    n=0
    for f,v in files:
        k,tp=f.split('.')
        if f not in th : continue
        n+=1
        #if n>100 : break
        if f[1:4]!='000' and f[1:4]!='001': continue
        #if random.random()>0.3 : continue
        
        raw=list(open(v))[1:]
        vec=gen_price(raw,ndays,use_nan=False)
        if vec[-1][0]!=dates[-1] : 
            print('dates not matched',k)
            continue

        ps=numpy.array([p for d,p,*_ in vec])
        ps=ps/ps[0]

        if any(numpy.isnan(x) for x in ps) : 
            print('nan',k)
            continue
        pss.append(ps)
        print(k,end='\r')
        vol=gen_vec(raw,ndays,ind=10)
        vol=numpy.array([p for d,p in vol])
        vols.append(vol)


    v,v2=mean_with_nan(vols)

    p=pss[0]
    for i in range(1,len(pss)):
        p+=pss[i]
    p=sum(pss)
    p=p/p[0]

    rates=[]
    for price in pss :
        #pri=numpy.array(price.tolist()[1:]+[price[-1]])
        pri=numpy.array(price.tolist()[3:]+[price[-1]]*3)
        rate=pri/price-1
        rates.append(rate)
    rate=sum(rates)
    mean_rate=rate/len(rates)
    #mean_rate=rate/rate[0]
    r_std=numpy.sqrt(sum((r-mean_rate)**2 for r in rates)/len(rates))
    
    # moving average
    r2=numpy.array(r_std.tolist()[1:]+[r_std[-1]])
    r3=numpy.array(r_std.tolist()[2:]+[r_std[-1]]*2)
    r_std+=r2+r3


    filename=haitai.output_dir+'/'+bk+'_whole.svg'
    div=r_std/r_std[0]
    div=1+(div-1)/4
    plot(p,div,v,v2,both_ticks=both_ticks)


    pylab.title(dates[0])
    pylab.savefig(filename)
    pylab.clf()
