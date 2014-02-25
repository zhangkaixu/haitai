#!/usr/bin/python3
import time
import sys
import os
import random
import datetime

import haitai
from haitai.data_source import netease_daily

help_text="""使用163下载股票每日历史数据

./163.py date [stocks]
    date ： 2013-11-01 或 20131101 或 today
    
例如：
    ./haitai/scripts/163.py 2013-11-01 # 下载所有指数信息
    ./haitai/scripts/163.py 2013-11-01 stocks # 下载所有股票信息"""

url="""http://quotes.money.163.com/service/chddata.html?code=%(a)s&end=%(today)s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"""


if __name__ == '__main__':
    if len(sys.argv)==1 :
        print(help_text)
        exit()

    if len(sys.argv)>2 :
        stock_ids=[x.strip() for x in open(haitai.stock_ids)]
        if (sys.argv[2]=='stocks') :
            pass
        if (sys.argv[2]=='top') :
            stock_ids=[i for i in stock_ids if i[1]=='0' and i[2]=='0' 
                    and (i[3]in '01')]

    else :
        stock_ids=[x.strip() for x in open(haitai.index_ids)]

    today=sys.argv[1]
    if today=='today' :
        t=datetime.date.today()
        m=t.month
        if m<10 : m='0'+str(m)
        d=t.day
        if d<10 : d='0'+str(d)
        today=''.join(map(str,(t.year,m,d)))
    else :
        today=today.replace('-','')

    dest=haitai.daily_dir

    print("下载截止日期为 %s 的 %s 只股票每日行情到目标 %s" %(today,len(stock_ids),dest))
    stock_ids=sorted(stock_ids)

    n=len(stock_ids)
    start_time=time.time()

    os.system('mkdir -p '+os.path.join(dest))

    for i,stock_id in enumerate(stock_ids) :
        last=netease_daily.refresh_stock(stock_id,today)
        if not last : continue
        now=time.time()
        sec_left=(now-start_time)/(i+1)*(n-i-1)
        print(stock_id,last)
        print("%.2f%% %.2f"%((i+1)/n*100,sec_left),end='\r')
