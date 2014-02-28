#!/usr/bin/python3
import os
import sys
import numpy
import time
import datetime
import pylab
from matplotlib.font_manager import FontProperties

import haitai
import haitai.graph
import haitai.common
from haitai.data_source import netease_daily


zhfont1 = FontProperties(fname='./simhei.ttf') #
    
def plot(price,filename,
        both_ticks=None,
        title='',
        background=None):

    div_price = price - background

    #subplot
    ax=pylab.subplot(2,1,1)
    haitai.graph.draw_lines(ax,[[div_price]])
    haitai.graph.draw_grid(ax,both_ticks)
    pylab.title(title,fontproperties=zhfont1)
            
    #subplot
    ax=pylab.subplot(2,1,2)
    haitai.graph.draw_lines(ax,[[price],[background,'g']],log=True)
    haitai.graph.draw_grid(ax,both_ticks)

    pylab.savefig(filename)
    pylab.clf()

if __name__ == '__main__':
    bk='主板'

    pylab.figure(figsize=(9,6))

    dates,ps,_=zip(*list(x.split() for x in open(bk+'_mean.txt')))
    both_ticks=haitai.graph.gen_ticks(dates)
    today=dates[0]
    ps=numpy.array(list(map(float,ps)))

    #rtn = netease_daily.load_fresh_stock('000300.ss', dates, vind = 11)
    #name, price, volum = rtn
    #ps=price

    th = set(haitai.get_symbol_list(bk))
    for f in sorted(th) :
        outfile='output/figs/'+f+'.svg'

        # if the svg file is new, do nothing
        if os.path.exists(outfile) :
            mtime=os.path.getmtime(outfile)
            mtime=datetime.date.fromtimestamp(mtime)
            if today < str(mtime) :
                continue

        rtn = netease_daily.load_fresh_stock(f, dates)
        if rtn is None : continue
        name, price, volum = rtn

        min_days=len(price)
        print(f,name, today,end='\r')

        plot(price,outfile,
                background=ps[:min_days],
                title="%s (%s) %s"%(name,f, today),
                both_ticks = both_ticks
                )
        #time.sleep(0.5) # if you think it is too CPU-consumming
