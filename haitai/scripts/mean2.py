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


def test(pss):
    print("haha")
    print(pss[2])

    m=[[] for i in range(len(pss[0]))]
    nn=[0 for i in range(len(pss[0]))]

    for vec in pss:
        for i in range(len(vec)-1):
            if (np.isnan(vec[i])
                    or np.isnan(vec[i+1])):
                continue
            nn[i]+=1
            m[i].append( vec[i] / vec[i+1] - 1)
    m=[np.std(a) if np.std(a) < 0.07 else np.nan for a,b in zip(m,nn)]
    return m

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
    p = np.array(test(pss))
    print(p)
    print(np.max(p), np.min(p))
    tf = open('tmp.txt', 'w')
    print(*p, file = tf)
    tf.close()
    p[0] = 0
    haitai.graph.draw_lines(ax,[[p,'k']],log=True)
    #haitai.graph.draw_lines(ax,[[v,'k']],log=True)
    haitai.graph.draw_grid(ax,both_ticks)

    filename=haitai.output_dir+'/'+bk+'_mean.svg'
    pylab.savefig(filename)
    pylab.clf()

    # save mean curve
    file=open(bk+'_mean.txt','w')
    for dd,pp,vv in zip(dates,p,v):
        print(dd,pp,vv,file=file)
    file.close()
