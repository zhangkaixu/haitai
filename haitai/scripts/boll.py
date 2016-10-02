#!/usr/bin/python3
import matplotlib
matplotlib.use('Agg')
import os
import sys
import pylab
import numpy as np

import haitai.graph
import haitai.common
import haitai

def boll(ps):
    alpha = 0.98
    mmean = None
    mstd = None

    b_m = []
    b_s = []
    bs = [] 
    for i in range(len(ps) - 1, -1, -1):
        p = ps[i]

        if mmean is None :
            mmean = p
        else :
            mmean = alpha * mmean + (1 - alpha) * p

        if mstd is None :
            mstd = 0
        else :
            mstd = np.sqrt(
                    alpha * mstd ** 2 
                    + (1 - alpha) * (p - mmean) ** 2
                    )
        bs.append((p - mmean) / mstd if mstd > 0 else 0)

        b_m.append(mmean)
        b_s.append(mstd)
    b_m = np.array(list((b_m)))
    b_s = np.array(list((b_s)))
    
    return b_m, b_s, bs
    
def cal_mean(pss):
    m=[0 for i in range(len(pss[0]))]
    nn=[0 for i in range(len(pss[0]))]

    for vec in pss:
        for i in range(len(vec)):
            if (np.isnan(vec[i])
                    ):
                continue
            nn[i]+=1
            m[i]+= vec[i]
    m=[(a)/b if b > 0 else np.nan for a,b in zip(m,nn)]
    m = list(reversed(m))
    return m
def cal_std(pss):
    m=[[] for i in range(len(pss[0]))]
    nn=[0 for i in range(len(pss[0]))]

    for vec in pss:
        for i in range(len(vec)):
            if (np.isnan(vec[i])
                    ):
                continue
            nn[i]+=1
            m[i].append((vec[i]))
    m=[np.std(a) if np.std(a) < 10 else np.nan for a,b in zip(m,nn)]
    print(len(m))
    return m

def test(pss):

    bss = []
    for ps in pss:
        b_m, b_s, bs = boll(ps)
        #bs = b_s / b_m
        bss.append(bs)

    return cal_mean(bss), list(reversed(cal_std(bss)))


if __name__ == '__main__':
    ndays=3000
    bk='全部'
    bk='中小'
    bk='主板'

    # dates
    dates=haitai.common.recent_n_days(ndays)

    # stocks
    th = set(haitai.get_symbol_list(bk))

    d = 'data/163_daily'
    fs = os.listdir(d)
    fs = [f for f in fs if f != '000300.ss']
    print(fs)
    #th = set(list(th)[:100]) # for debug only

    # get data
    pss, vols = haitai.common.load_stock_set(fs,ndays,dates)

    # compute
    p=sum(pss)
    print(p)
    p=p/p[0]
    v=haitai.common.mean_with_nan(vols)

    # fig
    pylab.figure(figsize=(12,6))
    both_ticks=haitai.graph.gen_ticks(dates)

    ax=pylab.subplot(2,1,1)
    haitai.graph.draw_lines(ax,[[p]],log=True)
    haitai.graph.draw_grid(ax,both_ticks)

    ax=pylab.subplot(2,1,2)
    p,p_std = test(pss)
    print(len(p))
    p = np.array(p)
    print(p.shape)
    print(np.max(p), np.min(p))
    
    tf = open('tmp.txt', 'w')
    print(*p, sep = '\n', file = tf)
    tf.close()
    #p[0] = 0
    haitai.graph.draw_lines(ax,[[p,'k'], 
        [np.array(p_std) * 2,'red']], log = True)
    #haitai.graph.draw_lines(ax,[[v,'k']],log=True)
    haitai.graph.draw_grid(ax,both_ticks)

    filename=haitai.output_dir+'/'+bk+'_mean.svg'
    pylab.savefig(filename)
    pylab.clf()

    # save mean curve
    #file=open(bk+'_mean.txt','w')
    #for dd,pp,vv in zip(dates,p,v):
    #    print(dd,pp,vv,file=file)
    #file.close()
