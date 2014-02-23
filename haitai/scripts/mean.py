#!/usr/bin/python3
import os
import sys
import pylab

import haitai.graph
import haitai.common
import haitai

if __name__ == '__main__':
    ndays=1000
    bk='全部'
    bk='中小'
    bk='主板'

    # dates
    dates=haitai.common.recent_n_days(ndays)

    # stocks
    th = set(haitai.get_symbol_list(bk))
    th = set(list(th)[:100]) # for debug only

    # get data
    pss, vols = haitai.common.load_stock_set(th,ndays,dates)

    # compute
    p=sum(pss)
    p=p/p[0]
    v=haitai.common.mean_with_nan(vols)

    # fig
    pylab.figure(figsize=(12,6))
    both_ticks=haitai.graph.gen_ticks(dates)

    ax=pylab.subplot(2,1,1)
    haitai.graph.draw_lines(ax,[[p]],log=True)
    haitai.graph.draw_grid(ax,both_ticks)

    ax=pylab.subplot(2,1,2)
    haitai.graph.draw_lines(ax,[[v,'k']],log=True)
    haitai.graph.draw_grid(ax,both_ticks)

    filename=haitai.output_dir+'/'+bk+'_mean.svg'
    pylab.savefig(filename)
    pylab.clf()

    # save mean curve
    file=open(bk+'_mean.txt','w')
    for dd,pp,vv in zip(dates,p,v):
        print(dd,pp,vv,file=file)
    file.close()
