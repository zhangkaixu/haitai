#!/usr/bin/python3
import os
import sys
import numpy
import math
import random
import pylab
import numpy as np

import haitai
from haitai.common import *
from haitai.graph import *

def plot(data,r_std,vol,vol_std,both_ticks=None):
    ax=pylab.subplot(2,1,1)
    draw_lines(ax,[[data,'k'],[r_std,'b']],log=True)
    draw_lines(ax,[[data,'k-'],[data,'b,'],],log=True)
    draw_grid(ax,both_ticks)

    ax=pylab.subplot(2,1,2)
    draw_lines(ax,[[vol],[vol_std]])
    pylab.ylim([0,10])
    draw_grid(ax,both_ticks)


if __name__ == '__main__':
    ndays=500
    bk='主板'

    pylab.figure(figsize=(12,6))
    dates=recent_n_days(ndays)
    both_ticks=gen_ticks(dates)

    # 列表中有的股票代码
    th = set(haitai.get_symbol_list(bk))
    #th = {f for f in th if not (f[1:4] != '000' and f[1:4] != '001')}

    #pss,vols=haitai.common.load_stock_set(set(list(th)[:100]),ndays,dates)
    pss,vols=haitai.common.load_stock_set(set(list(th)),ndays,dates)

    # 价格平均
    p=sum(pss)
    p=p/p[0]
    v,v2=mean_and_var_with_nan(vols)

    # 涨跌幅
    rates=[]
    for price in pss :
        pri=numpy.array(price.tolist()[3:]+[price[-1]]*3)
        rate=pri/price-1
        rates.append(rate)
    mean_rate,r_std=mean_and_var_with_nan(rates)
    
    # 涨跌幅方差的moving average
    r2=numpy.array(r_std.tolist()[1:]+[r_std[-1]])
    r3=numpy.array(r_std.tolist()[2:]+[r_std[-1]]*2)
    r_std+=r2*0.5+r3*0.25

    filename=haitai.output_dir+'/'+bk+'_whole.svg'
    div=r_std/r_std[0]
    div=1+(div-1)/4
    plot(p,div,v,v2,both_ticks=both_ticks)

    pylab.title(dates[0])
    pylab.savefig(filename)
    pylab.clf()
