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

def diff_all():
    bk='主板'

    # init the figure
    pylab.figure(figsize=(9,6))

    # get the dates, prepare the ticks, get today, and the mean price
    dates,ps,_=zip(*list(x.split() for x in open(bk+'_mean.txt')))
    both_ticks=haitai.graph.gen_ticks(dates)
    today=dates[0]
    ps=numpy.array(list(map(float,ps)))

    # sets of stocks
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

def diff_svg(stock_a,stock_b):
    bk='主板'

    # init the figure
    pylab.figure(figsize=(9,6))

    # get the dates, prepare the ticks, get today, and the mean price
    dates,ps,_=zip(*list(x.split() for x in open(bk+'_mean.txt')))
    both_ticks=haitai.graph.gen_ticks(dates)
    today=dates[0]
    ps=numpy.array(list(map(float,ps)))

    # sets of stocks
    th = set(haitai.get_symbol_list(bk))

    outfile='output/tmp.svg'

    # data of the stock_a
    rtn = netease_daily.load_fresh_stock(stock_a, dates)
    if rtn is None : return
    name, price, volum = rtn

    min_days=len(price)
    print(stock_a, name, today,end='\r')

    plot(price,outfile,
            background=ps[:min_days],
            title="%s (%s) %s"%(name, stock_a, today),
            both_ticks = both_ticks
            )
    return (open(outfile).read())


if __name__ == '__main__':
    #diff_all()
    diff('600178.ss',None)
